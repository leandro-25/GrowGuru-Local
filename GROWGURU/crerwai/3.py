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

# ✅ Usar a classe oficial ChatLiteLLM
llm = ChatLiteLLM(
    model="groq/gemma2-9b-it",
    temperature=0.7
)

# 🆕 Lista de tickers para processar
tickers_to_process = ["PETR4", "VALE3", "ITUB4", "BBDC4"]

# 🔄 Loop através de cada ticker na lista
for i, current_ticker in enumerate(tickers_to_process):
    print(f"\n{'='*50}")
    print(f"🚀 Processando ticker: {current_ticker} ({i+1}/{len(tickers_to_process)})")
    print(f"{'='*50}\n")

    # 🛠️ Tool com base no ticker ATUAL (com filtro de notícias recentes)
    news_scraper_tool = ScrapeWebsiteTool(
        website_url=f"https://news.google.com/search?q={current_ticker}&tbs=qdr:m"
    )

    # 👤 Agente (permanece o mesmo)
    news_agent = Agent(
        role="Analista de Notícias Financeiras Sênior",
        goal="Encontrar, resumir e classificar o impacto de notícias relevantes sobre ativos de mercado",
        backstory=(
            "Você é um analista financeiro experiente, especializado em coletar notícias recentes, "
            "identificar o sentimento do mercado e classificar o impacto potencial de cada evento para orientar investidores de forma clara e objetiva."
        ),
        tools=[news_scraper_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 🧾 Task (✅ ALTERAÇÕES APLICADAS AQUI)
    # A descrição foi detalhada para pedir a nova estrutura de saída.
    news_task = Task(
        description=(
            f"Busque as notícias mais recentes (da última semana) sobre o ativo {current_ticker}. "
            "Para cada notícia relevante, analise e gere um item na lista. "
            "No final, consolide tudo em um resumo e um impacto geral. "
            "Siga ESTA ESTRUTURA RIGOROSAMENTE:\n\n"
            "**Análise de Notícias para {current_ticker}**\n\n"
            "**Notícia 1:**\n"
            "- **Título:** [Título da notícia]\n"
            "- **Resumo:** [Resumo de até 2 linhas]\n"
            "- **Impacto Potencial:** [Classifique como: Muito Baixo, Baixo, Neutro, Alto, ou Muito Alto]\n\n"
            "**Notícia 2:**\n"
            "- **Título:** [Título da notícia]\n"
            "- **Resumo:** [Resumo de até 2 linhas]\n"
            "- **Impacto Potencial:** [Classifique como: Muito Baixo, Baixo, Neutro, Alto, ou Muito Alto]\n\n"
            "(Continue para outras notícias relevantes...)\n"
            "---\n\n"
            "**Resumo Geral:**\n"
            "[Escreva um parágrafo de 3 a 4 linhas consolidando as informações de todas as notícias, explicando o cenário atual do ativo.]\n\n"
            "**Impacto Geral Consolidado:**\n"
            "[Com base na média e na relevância dos impactos individuais, defina o impacto geral para o ativo usando UMA das classificações: Muito Baixo, Baixo, Neutro, Alto, ou Muito Alto.]"
        ),
        expected_output=(
            "Um relatório completo e bem formatado para o ativo {current_ticker}, "
            "contendo uma lista de notícias individuais com título, resumo e classificação de impacto, "
            "seguido por um parágrafo de resumo geral e, por fim, uma única classificação de impacto geral consolidado."
        ),
        tools=[news_scraper_tool],
        agent=news_agent
    )


    # 👥 Crew
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