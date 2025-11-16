# 📦 Instalar dependências
# pip install -q crewai crewai_tools litellm beautifulsoup4 requests langchain-community

# 🌍 Imports
import os
import time # Importar o módulo time para usar sleep
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
import litellm

# Importar a integração oficial do Litellm para LangChain/CrewAI
from langchain_community.chat_models.litellm import ChatLiteLLM


# 🧠 Definir API key da Groq
os.environ["GROQ_API_KEY"] = "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"

# 🔧 Configurar Litellm
litellm.set_verbose = False

# ✅ CORREÇÃO: Usar a classe oficial ChatLiteLLM em vez de uma personalizada.
# Isso garante compatibilidade total com todos os recursos do CrewAI.
llm = ChatLiteLLM(
    model="groq/gemma2-9b-it",
    temperature=0.7
)

# 🆕 Lista de tickers para processar
# Coloquei 4 exemplos, você pode ajustar conforme necessário
tickers_to_process = ["PETR4", "VALE3", "ITUB4", "BBDC4"]

# 🔄 Loop através de cada ticker na lista
for i, current_ticker in enumerate(tickers_to_process):
    print(f"\n{'='*50}")
    print(f"🚀 Processando ticker: {current_ticker} ({i+1}/{len(tickers_to_process)})")
    print(f"{'='*50}\n")

    # 🛠️ Tool com base no ticker ATUAL
    # A ferramenta precisa ser recriada para cada ticker para apontar para a URL correta
    news_scraper_tool = ScrapeWebsiteTool(
        website_url=f"https://news.google.com/search?q={current_ticker}"
    )

    # 👤 Agente
    # O agente também é recriado para garantir que use a ferramenta atualizada
    news_agent = Agent(
        role="Analista de Notícias Financeiras",
        goal="Encontrar e resumir notícias relevantes sobre ativos de mercado",
        backstory=(
            "Você é um analista financeiro especializado em coletar notícias recentes "
            "e identificar possíveis impactos no mercado para orientar investidores."
        ),
        tools=[news_scraper_tool], # Passa a ferramenta ATUALIZADA
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 🧾 Task
    # A tarefa é recriada para incluir o ticker atualizado na descrição
    news_task = Task(
        description=(
            f"Você deve buscar as notícias mais recentes relacionadas ao ativo {current_ticker}. "
            "Analise o conteúdo da página fornecida pela ferramenta e gere um relatório "
            "com os seguintes pontos:\n\n"
            "1. Títulos das principais notícias\n"
            "2. Resumo de até 2 linhas de cada notícia\n"
            "3. Qualquer sentimento ou impacto potencial detectado\n\n"
            "Seu relatório deve ser bem formatado e informativo para um investidor que quer entender o contexto atual do ativo."
        ),
        expected_output=f"Um relatório formatado com títulos, resumos e insights sobre o ativo {current_ticker}.",
        tools=[news_scraper_tool], # Passa a ferramenta ATUALIZADA
        agent=news_agent # Passa o agente ATUALIZADO
    )

    # 👥 Crew
    # O Crew é recriado para usar o agente e a tarefa atuais
    crew = Crew(
        agents=[news_agent],
        tasks=[news_task],
        process=Process.sequential,
        verbose=True
    )

    # 🏁 Executar
    result = crew.kickoff()
    print(f"\n✅ RESULTADO FINAL PARA {current_ticker}:\n")
    print(result)

    # ⏰ Intervalo de 70 segundos entre as chamadas da API (se não for o último ticker)
    if i < len(tickers_to_process) - 1:
        print(f"\n🚧 Aguardando 70 segundos antes de processar o próximo ticker...")
        time.sleep(70)

print("\n🚀 Todos os tickers foram processados!")