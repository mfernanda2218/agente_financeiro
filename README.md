# Agente Financeiro Inteligente

Um assistente financeiro pessoal avançado desenvolvido com Streamlit e API do Groq, capaz de analisar transações financeiras, fornecer recomendações personalizadas de investimento e contextualizar decisões com indicadores econômicos em tempo real.

---

## Funcionalidades

### Análise Financeira
- **Análise de transações financeiras** com identificação de padrões de gastos
- **Recomendações de investimento personalizadas** baseadas no perfil do investidor
- **Consulta a produtos financeiros** disponíveis no mercado
- **Upload de arquivos CSV** para análise personalizada

### Indicadores Econômicos
- **Integração com PostgreSQL** para consulta de indicadores do Banco Central
- **Selic e IPCA em tempo real** para contextualizar recomendações
- **Análise de impacto** dos indicadores nas decisões financeiras
- **Fallback automático** com SQLite quando o banco não está disponível
- **Dados simulados** com valores realistas para demonstração e segurança

### Inteligência Contextual
- **Recomendações adaptativas** baseadas no cenário macroeconômico
- **Regras Anti-Alucinação** para garantir que a IA não inverta rentabilidade com capital aportado
- **Justificativas claras** para cada recomendação
- **Análise de tendências** com dados históricos

### Interface (UI Premium)
- **Interface web interativa** com Streamlit modularizada
- **Design limpo (Clean UI)** sem o uso de emojis poluentes e customizado com tipografia Inter
- **Painel de indicadores econômicos** na sidebar
- **Visualização de gráficos** interativos e análises detalhadas
- **Histórico de conversas** com contexto persistente
- **Limpeza de histórico** com um clique

---

## Pré-requisitos

- **Python 3.8+**
- **Chave de API do Groq** (obrigatória)
- **PostgreSQL 13+** (opcional - para indicadores econômicos)
- **Banco de dados criado** para o pipeline ETL (se usar PostgreSQL)

---

## Instalação

### 1. Clone o repositório:

```bash
git clone <repositório>
cd agente_financeiro
```

### 2. Crie e ative o ambiente virtual:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```bash
# API Groq (obrigatório)
GROQ_API_KEY=sua_chave_api_aqui
LLM_MODEL=llama-3.1-8b-instant

# PostgreSQL (opcional - para indicadores econômicos)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bd_pipeline_etl
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

**Obtendo a chave da API Groq:**
1. Acesse [console.groq.com](https://console.groq.com)
2. Faça login ou crie uma conta
3. Vá para API Keys e gere uma nova chave

**Configurando o PostgreSQL (opcional):**
- Se você já possui o pipeline ETL de indicadores, use as mesmas credenciais
- Se não tiver, o agente usa automaticamente dados simulados

### 5. Configure os dados de exemplo:

Certifique-se de que os seguintes arquivos existem na pasta `data/`:

```
data/
├── transacoes.csv           # Histórico de transações
├── perfil_investidor.json   # Perfil do investidor
└── produtos_financeiros.json # Produtos disponíveis
```

---

## Executando o Projeto

### Execução padrão:

```bash
streamlit run src/app.py
```

O aplicativo estará disponível em `http://localhost:8501`

### Sem PostgreSQL (Fallback automático):

O agente funciona perfeitamente sem PostgreSQL, usando dados pré-estabelecidos em SQLite (ex. Selic em 13.75%).

---

## Estrutura do Projeto

```
agente_financeiro/
├── src/
│   ├── components/             # Módulos de interface (Clean UI)
│   │   ├── analise_gastos.py   # Componente de gráficos e métricas
│   │   ├── perfil_upload.py    # Abas e inputs do perfil
│   │   ├── produtos_upload.py  # Gestão do catálogo de produtos
│   │   └── transacoes_upload.py# Upload e validação de extrato
│   ├── app.py                  # Aplicação principal Streamlit
│   ├── config.py               # Configurações do projeto
│   ├── data_loader.py          # Carregamento robusto de dados locais
│   ├── db_indicadores.py       # Integração com banco de dados
│   ├── llm_client.py           # Cliente da API Groq com system prompts
│   └── styles.css              # Customização de design premium
├── data/
│   ├── transacoes.csv          # Histórico de transações
│   ├── perfil_investidor.json  # Perfil do usuário
│   └── produtos_financeiros.json # Produtos disponíveis
├── docs/                       # Documentação do projeto
├── .env                        # Variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
├── requirements.txt            # Dependências Python
└── README.md                   # Documentação do projeto
```

---

## Status do Projeto

**Este é um projeto em evolução contínua.**

### Funcionalidades Implementadas:

- Interface web modularizada com UI Premium (Streamlit + CSS customizado)
- Integração com API do Groq e Prompt Design refinado anti-alucinação
- Análise de dados financeiros e renderização de gráficos
- Recomendações baseadas em contexto macroeconômico
- Fallback de banco de dados e validações seguras para CSV

### Melhorias Planejadas:

- Autenticação e login de usuários
- Banco de dados persistente para salvar o histórico de conversas
- Integração com APIs bancárias reais (Open Finance)
- Deploy em produção (Docker, AWS, etc.)
- Alertas e notificações automáticas
