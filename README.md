# 💰 Agente Financeiro Inteligente

Um assistente financeiro pessoal avançado desenvolvido com Streamlit e API do Groq, capaz de analisar transações financeiras, fornecer recomendações personalizadas de investimento e contextualizar decisões com indicadores econômicos em tempo real.

---

## 🚀 Funcionalidades

### 📈 Análise Financeira
- **Análise de transações financeiras** com identificação de padrões de gastos
- **Recomendações de investimento personalizadas** baseadas no perfil do investidor
- **Consulta a produtos financeiros** disponíveis no mercado
- **Upload de arquivos CSV** para análise personalizada

### 📊 Indicadores Econômicos (NOVO!)
- **Integração com PostgreSQL** para consulta de indicadores do Banco Central
- **Selic e IPCA em tempo real** para contextualizar recomendações
- **Análise de impacto** dos indicadores nas decisões financeiras
- **Fallback automático** com SQLite quando o banco não está disponível
- **Dados mockados** com valores realistas para demonstração

### 🎯 Inteligência Contextual
- **Recomendações adaptativas** baseadas no cenário macroeconômico
- **Alertas proativos** sobre oportunidades de investimento
- **Justificativas claras** para cada recomendação
- **Análise de tendências** com dados históricos

### 💻 Interface
- **Interface web interativa** com Streamlit
- **Painel de indicadores econômicos** na sidebar
- **Visualização de métricas** (Selic, IPCA)
- **Histórico de conversas** com contexto persistente
- **Limpeza de histórico** com um clique

---

## 📋 Pré-requisitos

- **Python 3.8+**
- **Chave de API do Groq** (obrigatória)
- **PostgreSQL 13+** (opcional - para indicadores econômicos)
- **Banco de dados criado** para o pipeline ETL (se usar PostgreSQL)

---

## ⚙️ Instalação

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
- Se não tiver, o agente usa automaticamente dados mockados em SQLite

### 5. Configure os dados de exemplo:

Certifique-se de que os seguintes arquivos existem na pasta `data/`:

```
data/
├── transacoes.csv           # Histórico de transações
├── perfil_investidor.json   # Perfil do investidor
└── produtos_financeiros.json # Produtos disponíveis
```

### 6. Estrutura de dados de exemplo:

**`data/perfil_investidor.json`:**
```json
{
  "nome": "João Silva",
  "idade": 35,
  "perfil_risco": "moderado",
  "renda_mensal": 15000,
  "patrimonio": 250000,
  "objetivos": ["aposentadoria", "imóvel"]
}
```

**`data/produtos_financeiros.json`:**
```json
[
  {
    "nome": "Tesouro Selic",
    "tipo": "Renda Fixa",
    "risco": "Baixo",
    "retorno_estimado": "13.65% a.a.",
    "liquidez": "Diária"
  },
  {
    "nome": "CDB 100% CDI",
    "tipo": "Renda Fixa",
    "risco": "Baixo",
    "retorno_estimado": "13.15% a.a.",
    "liquidez": "Diária"
  }
]
```

---

## 🏃‍♂️ Executando o Projeto

### Execução padrão:

```bash
streamlit run src/app.py
```

O aplicativo estará disponível em `http://localhost:8501`

### Com indicadores econômicos (PostgreSQL):

Certifique-se de que o PostgreSQL está rodando e a tabela `indicadores_economicos` está populada:

```bash
# Verificar se o PostgreSQL está rodando
netstat -ano | findstr :5432   # Windows
pg_isready                      # Linux/Mac

# Executar o pipeline ETL (se tiver)
python etl_bcb.py              # Pipeline de indicadores
```

### Sem PostgreSQL (Fallback automático):

O agente funciona perfeitamente sem PostgreSQL, usando dados mockados em SQLite. Os indicadores exibidos serão:
- Selic: 13.75% ao ano
- IPCA: 0.56% mensal

---

## 📁 Estrutura do Projeto

```
agente_financeiro/
├── src/
│   ├── app.py                  # Aplicação principal Streamlit
│   ├── config.py               # Configurações do projeto
│   ├── data_loader.py          # Carregamento de dados locais
│   ├── db_indicadores.py       # Integração com banco de dados (NOVO!)
│   └── llm_client.py           # Cliente da API Groq
├── data/
│   ├── transacoes.csv          # Histórico de transações
│   ├── perfil_investidor.json  # Perfil do usuário
│   └── produtos_financeiros.json # Produtos disponíveis
├── docs/                        # Documentação do projeto
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   └── 04-metricas.md
├── .env                         # Variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação do projeto
```

---

## 🎯 Como Usar

### 1. Faça uma pergunta financeira

Digite sua pergunta no campo de texto. Exemplos:

- *"Como posso otimizar meu orçamento mensal?"*
- *"Quais investimentos são adequados para meu perfil moderado?"*
- *"Devo investir em CDB ou Tesouro Direto?"*
- *"Qual o impacto da Selic nos meus investimentos?"*

### 2. O agente analisará:

- ✅ **Seu perfil de investidor** (idade, renda, risco)
- ✅ **Suas transações** (padrões de gasto)
- ✅ **Produtos disponíveis** (opções de investimento)
- ✅ **Indicadores econômicos** (Selic, IPCA) - NOVO!

### 3. Receba recomendações personalizadas:

O agente fornece respostas contextualizadas com:
- 📊 Análise do cenário econômico atual
- 💡 Justificativa para cada recomendação
- 🎯 Produtos alinhados ao seu perfil
- ⚠️ Alertas sobre oportunidades e riscos

---

## 📊 Exemplo de Resposta com Indicadores

**Pergunta:** *"Qual o melhor investimento para meu perfil moderado?"*

**Resposta:**

```markdown
📊 ANÁLISE:
Com base na sua análise e no cenário econômico atual:

📈 INDICADORES ECONÔMICOS:
- Selic: 13.75% ao ano
- IPCA (mensal): 0.56%
- Data da consulta: 2026-07-07 14:30:00

📈 ANÁLISE DE IMPACTO:
• SELIC em 13.75%: Momento favorável para renda fixa. Considere CDB, Tesouro Selic e LCI/LCA.
• IPCA em 0.56%: Inflação elevada. Busque ativos com proteção contra perda de poder de compra.

🎯 RECOMENDAÇÕES PARA SEU PERFIL (Moderado):

1. Tesouro IPCA+ (70% do investimento)
   • Proteção contra inflação
   • Rentabilidade real garantida
   • Baixo risco

2. CDB 100% CDI (30% do investimento)
   • Liquidez diária
   • Rentabilidade atrelada à Selic
   • Segurança do FGC

💡 JUSTIFICATIVA:
Com a Selic alta (13.75%) e inflação pressionada (IPCA 0.56%),
a combinação de Tesouro IPCA+ com CDB oferece o equilíbrio ideal
entre rentabilidade e segurança para seu perfil moderado.
```

---

## 🔧 Dados de Exemplo

O projeto inclui dados de exemplo para demonstração:

### Perfil do Investidor:
- **Nome:** João Silva
- **Idade:** 35 anos
- **Perfil de Risco:** Moderado
- **Renda Mensal:** R$ 15.000
- **Patrimônio:** R$ 250.000
- **Objetivos:** Aposentadoria e compra de imóvel

### Transações (exemplo):
- Salário mensal: R$ 15.000
- Despesas fixas: R$ 8.000 (53%)
- Gastos variáveis: R$ 3.000 (20%)
- Investimentos: R$ 4.000 (27%)

### Produtos Financeiros (exemplo):
| Produto | Tipo | Risco | Retorno | Liquidez |
|---------|------|-------|---------|----------|
| Tesouro Selic | Renda Fixa | Baixo | 13.65% a.a. | Diária |
| CDB 100% CDI | Renda Fixa | Baixo | 13.15% a.a. | Diária |
| Tesouro IPCA+ | Renda Fixa | Médio | IPCA + 6.0% | Diária |
| Fundos de Ações | Variável | Alto | Variável | D+30 |
| FIIs | Variável | Médio | 8-10% a.a. | D+30 |

---

## 📊 Monitoramento e Logs

O sistema gera logs detalhados para monitoramento:

```bash
# Logs do agente
tail -f etl_pipeline.log  # Se configurado

# Logs do Streamlit
streamlit run src/app.py --logger.level=debug
```

**Níveis de log:**
- `INFO`: Operações normais
- `WARNING`: Avisos (ex: banco indisponível)
- `ERROR`: Erros críticos

---

## 📈 Status do Protótipo

**Este é um protótipo em evolução contínua.**

### ✅ Funcionalidades Implementadas:

- ✅ Interface web funcional com Streamlit
- ✅ Integração com API do Groq
- ✅ Análise de dados financeiros
- ✅ Recomendações básicas
- ✅ **Integração com PostgreSQL para indicadores econômicos**
- ✅ **Contexto macroeconômico nas recomendações**
- ✅ **Fallback para SQLite quando banco indisponível**
- ✅ **Painel de indicadores econômicos**
- ✅ Upload de arquivos CSV personalizados
- ✅ Histórico de conversas persistente
- ✅ Limpeza de histórico

### 🔄 Melhorias Planejadas:

- 🔄 Autenticação e login de usuários
- 🔄 Banco de dados persistente para histórico
- 🔄 Gráficos e visualizações interativas
- 🔄 Histórico de conversas salvo
- 🔄 Integração com APIs bancárias reais
- 🔄 Validação de dados em tempo real
- 🔄 Testes automatizados
- 🔄 Deploy em produção (Docker, AWS, etc.)
- 🔄 Alertas e notificações automáticas
- 🔄 Dashboard de performance financeira
- 🔄 Análise de correlação entre indicadores

---
