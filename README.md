# GROWGURU - Plataforma Inteligente de Investimentos

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vue.js)](https://vuejs.org/)
[![Ionic](https://img.shields.io/badge/Ionic-Framework-3880FF?logo=ionic)](https://ionicframework.com/)
[![Node.js](https://img.shields.io/badge/Node.js-Express-339933?logo=node.js)](https://expressjs.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Backend%20as%20a%20Service-3ECF8E?logo=supabase)](https://supabase.io/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-Utility%20First-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)

## Descrição

GROWGURU é uma aplicação full-stack projetada para simplificar e otimizar a experiência de investimento para usuários. A plataforma oferece ferramentas para cadastro, autenticação, visualização de estratégias de investimento, gerenciamento de carteira e acompanhamento de ativos financeiros. O objetivo é fornecer uma interface intuitiva e informações claras para auxiliar os usuários na tomada de decisões financeiras.

## Finalidade

A finalidade do projeto GROWGURU é democratizar o acesso a informações sobre investimentos e fornecer uma plataforma robusta onde os usuários possam:
*   Aprender sobre diferentes estratégias de investimento.
*   Construir e gerenciar suas carteiras de forma personalizada.
*   Acompanhar o desempenho de seus investimentos.


## Funcionalidades Principais

*   **Autenticação de Usuários:**
    *   Cadastro de novos usuários.
    *   Login seguro para usuários existentes.
*   **Gerenciamento de Perfil:**
    *   Visualização e atualização de dados do usuário.
    *   Consulta de saldo.
*   **Estratégias de Investimento:**
    *   Listagem de diversas estratégias de investimento disponíveis.
    *   Visualização detalhada dos ativos que compõem cada estratégia.
*   **Gerenciamento de Carteira:**
    *   Adição de ativos à carteira do usuário.
    *   Visualização da composição da carteira.
*   **Transações Financeiras:**
    *   Registro de aportes e retiradas.
    *   Histórico de transações.
*   **Interface Responsiva:**
    *   Design adaptável para diferentes dispositivos (desktop e mobile) utilizando Ionic e Tailwind CSS.

## Tecnologias Utilizadas

O projeto é dividido em duas partes principais: Frontend e Backend.

### Frontend
*   **Vue.js 3:** Framework progressivo para construção de interfaces de usuário.
*   **Ionic Framework:** SDK de UI para criar aplicações móveis, web e desktop de alta qualidade com uma única base de código.
*   **Vite:** Ferramenta de build moderna e rápida para desenvolvimento frontend (conforme <mcfile name="vite.config.ts" path="d:\FATEC\projetos\deeeep\frontend\vite.config.ts"></mcfile>).
*   **Tailwind CSS:** Framework CSS utility-first para estilização rápida e customizável .
*   **Pinia:** Solução de gerenciamento de estado para Vue.js
*   **Axios:** Para realizar requisições HTTP ao backend.
*   **Supabase Client JS:** Para interagir com os serviços do Supabase no lado do cliente.

### Backend
*   **Node.js:** Ambiente de execução JavaScript server-side.
*   **Express.js:** Framework minimalista e flexível para Node.js, usado para construir a API REST.
*   **Supabase:**
    *   **Database:** Banco de dados PostgreSQL gerenciado.
    *   **Authentication:** Gerenciamento de autenticação de usuários.
    *   **Storage (potencial):** Para armazenamento de arquivos.
*   **`dotenv`:** Para gerenciamento de variáveis de ambiente.
*   **`cors`:** Para habilitar Cross-Origin Resource Sharing.

## Estrutura do Projeto

O workspace está organizado da seguinte forma:


## Como Começar

Siga as instruções abaixo para configurar e executar o projeto localmente.

### Pré-requisitos
*   Node.js (versão LTS recomendada)
*   NPM ou Yarn
*   Conta no Supabase (para configurar o banco de dados e autenticação)

### Configuração do Backend

1.  **Navegue até a pasta do backend:**
    ```bash
    cd backend
    ```
2.  **Instale as dependências:**
    ```bash
    npm install
    ```
3.  **Configure as variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz da pasta `backend`.
    *   Adicione as seguintes variáveis com suas credenciais do Supabase:
        ```env
        SUPABASE_URL=SUA_SUPABASE_URL
        SUPABASE_KEY=SUA_SUPABASE_ANON_KEY_OU_SERVICE_ROLE_KEY
        PORT=3000 # Ou a porta que desejar
        ```
4.  **Execute o servidor de desenvolvimento:**
    (Assumindo que você tenha um script `start` ou `dev` no `backend/package.json`. Se não, adicione um como ` "start": "node index.js" `)
    ```bash
    npm start
    # ou
    # npm run dev
    ```
    O backend estará rodando em `http://localhost:3000` (ou a porta configurada).

### Configuração do Frontend

1.  **Navegue até a pasta do frontend:**
    ```bash
    cd frontend
    ```
2.  **Instale as dependências:**
    ```bash
    npm install
    ```
3.  **Configure as variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz da pasta `frontend`.
    *   Adicione as seguintes variáveis com suas credenciais do Supabase (chaves públicas):
        ```env
        VITE_SUPABASE_URL=SUA_SUPABASE_URL
        VITE_SUPABASE_ANON_KEY=SUA_SUPABASE_ANON_KEY
        ```
        *Nota: O prefixo `VITE_` é importante para que o Vite exponha essas variáveis ao código do cliente, conforme configurado em <mcfile name="supabase.js" path="d:\FATEC\projetos\deeeep\frontend\src\supabase.js"></mcfile>.*
4.  **Execute o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```
    O frontend estará acessível em `http://localhost:8100` (porta padrão do Ionic/Vite, pode variar).


## Endpoints da API (Exemplos)

Com base nas funcionalidades do frontend e no arquivo <mcfile name="api.d.ts" path="d:\FATEC\projetos\deeeep\frontend\src\api.d.ts"></mcfile>, alguns endpoints esperados no backend (`http://localhost:PORTA_BACKEND/api`):

*   `POST /api/signup`: Cadastro de novos usuários.
*   `POST /api/login`: Autenticação de usuários.
*   `GET /api/usuarios`: Obter dados do usuário logado.
*   `GET /api/estrategias`: Listar todas as estratégias de investimento.
*   `GET /api/estrategias?id=eq.{id}`: Obter detalhes de uma estratégia específica.
*   `GET /api/estrategias/:id/ativos`: Listar ativos de uma estratégia específica.
*   `POST /api/carteira`: Adicionar um ativo à carteira do usuário (investir).
*   `GET /api/carteira`: Obter a carteira do usuário logado.
*   `POST /api/transacoes`: Registrar uma nova transação financeira.
*   `GET /api/transacoes`: Listar transações do usuário.

*(Estes são exemplos inferidos e podem precisar de ajuste conforme a implementação real do backend em `index.js`.)*


## Licença

Este projeto está licenciado sob a Licença ISC. Veja a seção `license` no <mcfile name="package.json" path="d:\FATEC\projetos\deeeep\backend\package.json"></mcfile> ou consulte [ISC License](https://opensource.org/licenses/ISC).
