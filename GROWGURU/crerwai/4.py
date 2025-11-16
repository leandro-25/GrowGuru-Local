# 📦 Instalar dependências
# pip install -q crewai crewai_tools litellm beautifulsoup4 requests langchain-community

# 🌍 Imports
import os
import time
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
import litellm
from litellm.exceptions import RateLimitError # Importar a exceção específica

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
tickers_to_process = ["AALR3.SA", "ABCB4.SA", "ABEV3.SA", "ADHM3.SA", "AERI3.SA",
"AFLT3.SA", "AGRO3.SA", "AGXY3.SA", "AHEB3.SA", "AHEB5.SA",
"AHEB6.SA", "ALLD3.SA", "ALOS3.SA", "ALPA3.SA", "ALPA4.SA",
"ALPK3.SA", "ALUP11.SA", "ALUP3.SA", "ALUP4.SA", "AMAR3.SA",
"AMBP3.SA", "AMER3.SA", "AMOB3.SA", "ANIM3.SA", "ARML3.SA",
"ASAI3.SA", "ATED3.SA", "ATMP3.SA", "AURA33.SA", "AURE3.SA",
"AVLL3.SA", "AZEV3.SA", "AZEV4.SA", "AZUL4.SA", "AZZA3.SA",
"B3SA3.SA", "BALM3.SA", "BALM4.SA", "BAUH4.SA", "BAZA3.SA",
"BBAS3.SA", "BBDC3.SA", "BBDC4.SA", "BBSE3.SA", "BDLL3.SA",
"BDLL4.SA", "BEEF3.SA", "BEES3.SA", "BEES4.SA", "BGIP3.SA",
"BGIP4.SA", "BHIA3.SA", "BIED3.SA", "BIOM3.SA", "BLAU3.SA",
"BLUT3.SA", "BLUT4.SA", "BMEB3.SA", "BMEB4.SA", "BMGB4.SA",
"BMIN3.SA", "BMIN4.SA", "BMKS3.SA", "BMOB3.SA", "BNBR3.SA",
"BOBR4.SA", "BPAC11.SA", "BPAC3.SA", "BPAC5.SA", "BPAN4.SA",
"BRAP3.SA", "BRAP4.SA", "BRAV3.SA", "BRBI11.SA", "BRFS3.SA",
"BRIT3.SA", "BRKM3.SA", "BRKM5.SA", "BRKM6.SA", "BRSR3.SA",
"BRSR5.SA", "BRSR6.SA", "BRST3.SA", "BSLI3.SA", "BSLI4.SA",
"CAMB3.SA", "CAML3.SA", "CASH3.SA", "CBAV3.SA", "CBEE3.SA",
"CCRO3.SA", "CEAB3.SA", "CEBR3.SA", "CEBR5.SA", "CEBR6.SA",
"CEDO3.SA", "CEDO4.SA", "CEEB3.SA", "CEEB5.SA", "CEED3.SA",
"CGAS3.SA", "CGAS5.SA", "CGRA3.SA", "CGRA4.SA", "CLSA3.SA",
"CLSC3.SA", "CLSC4.SA", "CMIG3.SA", "CMIG4.SA", "CMIN3.SA",
"COCE3.SA", "COCE5.SA", "COGN3.SA", "CPFE3.SA", "CPLE3.SA",
"CPLE5.SA", "CPLE6.SA", "CRFB3.SA", "CRPG3.SA", "CRPG5.SA",
"CRPG6.SA", "CSAN3.SA", "CSED3.SA", "CSMG3.SA", "CSNA3.SA",
"CSUD3.SA", "CTKA3.SA", "CTKA4.SA", "CTNM3.SA", "CTNM4.SA",
"CTSA3.SA", "CTSA4.SA", "CURY3.SA", "CVCB3.SA", "CXSE3.SA",
"CYRE3.SA", "DASA3.SA", "DESK3.SA", "DEXP3.SA", "DEXP4.SA",
"DIRR3.SA", "DMVF3.SA", "DOHL3.SA", "DOHL4.SA", "DOTZ3.SA",
"DTCY3.SA", "DXCO3.SA", "EALT3.SA", "EALT4.SA", "ECOR3.SA",
"EGIE3.SA", "EKTR4.SA", "ELET3.SA", "ELET5.SA", "ELET6.SA",
"ELMD3.SA", "EMAE4.SA", "EMBR3.SA", "ENEV3.SA", "ENGI11.SA",
"ENGI3.SA", "ENGI4.SA", "ENJU3.SA", "ENMT3.SA", "ENMT4.SA",
"EPAR3.SA", "EQMA3B.SA", "EQPA3.SA", "EQPA5.SA", "EQPA7.SA",
"EQTL3.SA", "ESPA3.SA", "ESTR4.SA", "ETER3.SA", "EUCA3.SA",
"EUCA4.SA", "EVEN3.SA", "EZTC3.SA", "FESA3.SA", "FESA4.SA",
"FHER3.SA", "FICT3.SA", "FIEI3.SA", "FIQE3.SA", "FLRY3.SA",
"FRAS3.SA", "FRIO3.SA", "GEPA3.SA", "GEPA4.SA", "GFSA3.SA",
"GGBR3.SA", "GGBR4.SA", "GGPS3.SA", "GMAT3.SA", "GOAU3.SA",
"GOAU4.SA", "GOLL4.SA", "GPAR3.SA", "GPIV33.SA", "GRND3.SA",
"GSHP3.SA", "GUAR3.SA", "HAGA3.SA", "HAGA4.SA", "HAPV3.SA",
"HBOR3.SA", "HBRE3.SA", "HBSA3.SA", "HBTS5.SA", "HETA4.SA",
"HOOT4.SA", "HYPE3.SA", "IFCM3.SA", "IGBR3.SA", "IGTI11.SA",
"IGTI3.SA", "INEP3.SA", "INEP4.SA", "INTB3.SA", "IRBR3.SA",
"ISAE3.SA", "ISAE4.SA", "ITSA3.SA", "ITSA4.SA", "ITUB3.SA",
"ITUB4.SA", "JALL3.SA", "JBSS3.SA", "JFEN3.SA", "JHSF3.SA",
"JOPA3.SA", "JOPA4.SA", "JPSA3.SA", "JSLG3.SA", "KEPL3.SA",
"KLBN11.SA", "KLBN3.SA", "KLBN4.SA", "KRSA3.SA", "LAND3.SA",
"LAVV3.SA", "LEVE3.SA", "LIGT3.SA", "LIPR3.SA", "LJQQ3.SA",
"LOGG3.SA", "LOGN3.SA", "LPSB3.SA", "LREN3.SA", "LUPA3.SA",
"LUXM4.SA", "LVTC3.SA", "LWSA3.SA", "MAPT3.SA", "MAPT4.SA",
"MATD3.SA", "MBLY3.SA", "MDIA3.SA", "MDNE3.SA", "MEAL3.SA",
"MELK3.SA", "MERC4.SA", "MGEL4.SA", "MGLU3.SA", "MILS3.SA",
"MLAS3.SA", "MMAQ3.SA", "MMAQ4.SA", "MNDL3.SA", "MNPR3.SA",
"MOAR3.SA", "MOVI3.SA", "MRFG3.SA", "MRSA3B.SA", "MRSA5B.SA",
"MRSA6B.SA", "MRVE3.SA", "MSPA3.SA", "MTRE3.SA",
"MTSA4.SA", "MULT3.SA", "MWET3.SA", "MWET4.SA", "MYPK3.SA", "NEOE3.SA",
"NEXP3.SA", "NGRD3.SA", "NORD3.SA", "NTCO3.SA", "NUTR3.SA", "ODPV3.SA",
"OFSA3.SA", "OIBR3.SA", "OIBR4.SA", "ONCO3.SA", "OPCT3.SA", "ORVR3.SA",
"OSXB3.SA", "PATI3.SA", "PATI4.SA", "PCAR3.SA", "PDGR3.SA", "PDTC3.SA",
"PEAB3.SA", "PEAB4.SA", "PETR3.SA", "PETR4.SA", "PETZ3.SA", "PFRM3.SA",
"PGMN3.SA", "PINE3.SA", "PINE4.SA", "PLAS3.SA", "PLPL3.SA", "PMAM3.SA",
"PNVL3.SA", "POMO3.SA", "POMO4.SA", "PORT3.SA", "POSI3.SA", "PRIO3.SA",
"PRNR3.SA", "PSSA3.SA", "PTBL3.SA", "PTNT3.SA", "PTNT4.SA", "QUAL3.SA",
"RADL3.SA", "RAIL3.SA", "RAIZ4.SA", "RANI3.SA", "RAPT3.SA", "RAPT4.SA",
"RCSL3.SA", "RCSL4.SA", "RDNI3.SA", "RDOR3.SA", "REAG3.SA", "RECV3.SA",
"REDE3.SA", "RENT3.SA", "RNEW11.SA", "RNEW3.SA", "RNEW4.SA", "ROMI3.SA",
"RPAD3.SA", "RPAD5.SA", "RPAD6.SA", "RPMG3.SA", "RSID3.SA", "RSUL4.SA",
"SANB11.SA", "SANB3.SA", "SANB4.SA", "SAPR11.SA", "SAPR3.SA", "SAPR4.SA",
"SBFG3.SA", "SBSP3.SA", "SCAR3.SA", "SEER3.SA", "SEQL3.SA", "SGPS3.SA",
"SHOW3.SA", "SHUL4.SA", "SIMH3.SA", "SLCE3.SA", "SMFT3.SA", "SMTO3.SA",
"SNSY5.SA", "SOJA3.SA", "SOND5.SA", "SOND6.SA", "SRNA3.SA", "STBP3.SA",
"SUZB3.SA", "SYNE3.SA", "TAEE11.SA", "TAEE3.SA", "TAEE4.SA", "TASA3.SA",
"TASA4.SA", "TCSA3.SA", "TECN3.SA", "TEKA4.SA", "TELB3.SA", "TELB4.SA",
"TEND3.SA", "TFCO4.SA", "TGMA3.SA", "TIMS3.SA", "TKNO4.SA", "TOTS3.SA",
"TPIS3.SA", "TRAD3.SA", "TRIS3.SA", "TTEN3.SA", "TUPY3.SA", "TXRX3.SA",
"TXRX4.SA", "UCAS3.SA", "UGPA3.SA", "UNIP3.SA", "UNIP5.SA", "UNIP6.SA",
"USIM3.SA", "USIM5.SA", "USIM6.SA", "VALE3.SA", "VAMO3.SA", "VBBR3.SA",
"VITT3.SA", "VIVA3.SA", "VIVR3.SA", "VIVT3.SA", "VLID3.SA", "VSTE3.SA",
"VTRU3.SA", "VULC3.SA", "VVEO3.SA", "WEGE3.SA", "WEST3.SA", "WHRL3.SA",
"WHRL4.SA", "WIZC3.SA", "WLMM3.SA", "WLMM4.SA", "YDUQ3.SA", "ZAMP3.SA"]

# 🔄 Loop através de cada ticker na lista
for i, current_ticker in enumerate(tickers_to_process):
    print(f"\n{'='*50}")
    print(f"🚀 Processando ticker: {current_ticker} ({i+1}/{len(tickers_to_process)})")
    print(f"{'='*50}\n")

    news_scraper_tool = ScrapeWebsiteTool(
        website_url=f"https://news.google.com/search?q={current_ticker}&tbs=qdr:m"
    )

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

    news_task = Task(
        description=(
            f"Busque as notícias mais recentes (do último mês) sobre o ativo {current_ticker}. "
            "Para cada notícia relevante, analise e gere um item na lista. "
            "No final, consolide tudo em um resumo e um impacto geral. "
            "Siga ESTA ESTRUTURA RIGOROSAMENTE:\n\n"
            "**Análise de Notícias para {current_ticker}**\n\n"
            "**Notícia 1:**\n"
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

    crew = Crew(
        agents=[news_agent],
        tasks=[news_task],
        process=Process.sequential,
        verbose=True
    )

    # 🏁 Executar com tratamento de erro
    result = None
    try:
        print("▶️  Iniciando a execução do Crew...")
        result = crew.kickoff()
    except RateLimitError as e:
        print(f"\n❌ ERRO DE LIMITE DE TAXA DA API: {e}")
        print("🚧 Aguardando 60 segundos antes de continuar para o próximo ticker...")
        time.sleep(60)
        # Opcional: você poderia adicionar lógica para tentar novamente o MESMO ticker aqui
        # Mas por simplicidade, vamos apenas pular para o próximo.
        print(f"\n⚠️  O ticker {current_ticker} falhou devido ao limite da API e será pulado.")
        result = f"Falha ao processar {current_ticker} devido a RateLimitError."
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado ao processar {current_ticker}: {e}")
        result = f"Falha ao processar {current_ticker} devido a um erro inesperado."


    print(f"\n✅ RESULTADO FINAL PARA {current_ticker}:\n")
    print(result)

    # ⏰ Intervalo entre as chamadas da API (se não for o último ticker)
    if i < len(tickers_to_process) - 1:
        print(f"\n🚧 Aguardando 70 segundos antes de processar o próximo ticker...")
        time.sleep(70)

print("\n🚀 Todos os tickers foram processados!")