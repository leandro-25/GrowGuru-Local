# 📦 Instalar dependências
# pip install -q crewai crewai_tools litellm beautifulsoup4 requests langchain-community

# 🌍 Imports
import os
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

# 🛠️ Tool com base no ticker
ticker = "PETR4"
news_scraper_tool = ScrapeWebsiteTool(
    website_url=f"https://news.google.com/search?q={ticker}"
)

# 👤 Agente
news_agent = Agent(
    role="Analista de Notícias Financeiras",
    goal="Encontrar e resumir notícias relevantes sobre ativos de mercado",
    backstory=(
        "Você é um analista financeiro especializado em coletar notícias recentes "
        "e identificar possíveis impactos no mercado para orientar investidores."
    ),
    tools=[news_scraper_tool],
    llm=llm,
    verbose=True,
    # É uma boa prática desativar a delegação se você tem apenas um agente
    allow_delegation=False
)

# 🧾 Task
news_task = Task(
    description=(
        f"Você deve buscar as notícias mais recentes relacionadas ao ativo {ticker}. "
        "Analise o conteúdo da página fornecida pela ferramenta e gere um relatório "
        "com os seguintes pontos:\n\n"
        "1. Títulos das principais notícias\n"
        "2. Resumo de até 2 linhas de cada notícia\n"
        "3. Qualquer sentimento ou impacto potencial detectado\n\n"
        "Seu relatório deve ser bem formatado e informativo para um investidor que quer entender o contexto atual do ativo."
    ),
    expected_output="Um relatório formatado com títulos, resumos e insights sobre o ativo.",
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
print("\n✅ RESULTADO FINAL:\n")
print(result)