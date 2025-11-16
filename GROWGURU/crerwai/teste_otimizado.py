import os
import time
import threading
import concurrent.futures
from collections import deque
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
import litellm
from litellm.exceptions import RateLimitError
from langchain_community.chat_models.litellm import ChatLiteLLM

# Configurações
otimizacoes = {
    'max_workers': 5,  # Número de threads paralelas (ajuste conforme nescessário)
    'max_requests_per_minute': 25,  # Mantém abaixo do limite de 30 para segurança
    'retry_attempts': 10,  # Número de tentativas por ticker
    'base_delay': 10,  # Delay base entre requisições em segundos
}

# Configuração da API
def setup_llm():
    os.environ["GROQ_API_KEY"] = "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"
    #"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"
   # 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
    litellm.set_verbose = False
    return ChatLiteLLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)

# Controle de taxa de requisições
class RateLimiter:
    def __init__(self, max_requests: int, time_window: int = 60):
        self.requests = deque()
        self.max_requests = max_requests
        self.time_window = time_window
        self.lock = threading.Lock()

    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            # Remove registros mais antigos que a janela de tempo
            while self.requests and self.requests[0] <= now - self.time_window:
                self.requests.popleft()
            
            if len(self.requests) >= self.max_requests:
                sleep_time = (self.requests[0] + self.time_window) - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            self.requests.append(time.time())

# Processa um único ticker com tratamento de erros
def process_ticker(ticker: str, rate_limiter: RateLimiter, llm: ChatLiteLLM, retry_count: int = 0) -> Optional[str]:
    if retry_count >= otimizacoes['retry_attempts']:
        print(f"❌ Máximo de tentativas atingido para {ticker}")
        return None
    
    try:
        rate_limiter.wait_if_needed()
        print(f"🔄 Processando {ticker} (tentativa {retry_count + 1}/{otimizacoes['retry_attempts']})")
        
        # Cria o agente e a tarefa
        news_scraper_tool = ScrapeWebsiteTool(
            website_url=f"https://news.google.com/search?q={ticker}&tbs=qdr:m"
        )
        
        news_agent = Agent(
            role="Analista de Notícias Financeiras Sênior",
            goal="Encontrar e resumir notícias relevantes sobre ativos de mercado",
            backstory=("Você é um analista financeiro experiente, especializado em coletar "
                     "notícias recentes e identificar o sentimento do mercado."),
            tools=[news_scraper_tool],
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        # Instruções otimizadas para usar menos tokens
        task_description = (
            f"Analise brevemente o ativo {ticker} e retorne APENAS:\n"
            "1. **Resumo Geral** (máx 3 linhas)\n"
            "Formato exato de saída (obrigatório):\n"
            "RESUMO: [texto conciso]\n"
            "IMPACTO: [Positivo/Neutro/Negativo]"
        )
        
        # Formato simplificado de saída
        expected_output = (
            "RESUMO: Breve análise do cenário atual do ativo.\n"
            "IMPACTO: Positivo"
        )
        
        # Criando a tarefa
        news_task = Task(
            description=task_description,
            expected_output=expected_output,
            tools=[news_scraper_tool],
            agent=news_agent
        )
        
        crew = Crew(
            agents=[news_agent],
            tasks=[news_task],
            process=Process.sequential,
            verbose=False
        )
        
        return crew.kickoff()
        
    except RateLimitError as e:
        wait_time = (retry_count + 1) * 15  # Aumenta o tempo de espera a cada tentativa
        print(f"⚠️ RateLimitError em {ticker}. Tentando novamente em {wait_time} segundos...")
        time.sleep(wait_time)
        return process_ticker(ticker, rate_limiter, llm, retry_count + 1)
        
    except Exception as e:
        print(f"❌ Erro ao processar {ticker}: {str(e)}")
        return None

def process_single_ticker(ticker: str, llm: ChatLiteLLM, rate_limiter: RateLimiter) -> None:
    """Processa um único ticker e exibe os resultados."""
    print(f"\n🔍 Processando {ticker}...")
    start_time = time.time()
    
    try:
        result = process_ticker(ticker, rate_limiter, llm)
        if result:
            # Salva o resultado no arquivo
            with open('resultados_analise.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"📈 ANÁLISE PARA {ticker.upper()}\n")
                f.write(f"{'='*50}\n\n")
                result_str = str(result).strip()
                if not result_str.startswith("**Análise de Notícias para"):
                    f.write(f"**Análise de Notícias para {ticker.upper()}**\n\n")
                f.write(f"{result_str}\n")
            
            print(f"\n✅ Análise concluída para {ticker}")
            print(f"📝 Resultado salvo em 'resultados_analise.txt'")
        else:
            print(f"⚠️  Não foi possível obter resultados para {ticker}")
    except Exception as e:
        print(f"❌ Erro ao processar {ticker}: {str(e)}")
    
    elapsed = time.time() - start_time
    print(f"⏱️  Tempo de processamento: {elapsed:.2f} segundos")

def main():
    print("🔍 Análise de Tickers - Digite 'sair' a qualquer momento para encerrar")
    print("="*50)
    
    # Inicializa o LLM e o rate limiter uma única vez
    llm = setup_llm()
    rate_limiter = RateLimiter(max_requests=otimizacoes['max_requests_per_minute'])
    
    # Cria ou limpa o arquivo de resultados no início
    with open('resultados_analise.txt', 'w', encoding='utf-8') as f:
        f.write("=== ANÁLISES DE TICKERS ===\n\n")
    
    while True:
        print("\n" + "="*50)
        print("Digite o código do ativo que deseja analisar")
        print("Exemplo: ITUB4.SA, PETR4.SA ou VALE3.SA")
        print("Digite 'sair' para encerrar")
        print("-"*50)
        
        user_input = input("\nTicker: ").strip().upper()
        
        # Verifica se o usuário quer sair
        if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
            print("\n👋 Encerrando o programa...")
            break
            
        # Verifica se a entrada é válida
        if not user_input:
            print("❌ Por favor, digite um código de ativo válido.")
            continue
            
        # Processa o ticker
        process_single_ticker(user_input, llm, rate_limiter)
        print("\n" + "-"*50)
        print("Digite o próximo ticker ou 'sair' para encerrar")

if __name__ == "__main__":
    main()
