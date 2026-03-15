# Agente Financeiro Inteligente

Um protótipo de assistente financeiro pessoal desenvolvido com Streamlit e API do Groq, capaz de analisar transações financeiras e fornecer recomendações personalizadas de investimento.

## 🚀 Funcionalidades

- **Análise de transações financeiras**
- **Recomendações de investimento personalizadas**
- **Interface web interativa**
- **Baseado em perfil de investidor**
- **Consulta a produtos financeiros disponíveis**

## 📋 Pré-requisitos

- Python 3.8+
- Chave de API do Groq

## ⚙️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone <repositório>
   cd agente_financeiro
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a API do Groq:**
   ```bash
   # Crie um arquivo .env com:
   GROQ_API_KEY=sua_chave_api_aqui
   ```
   
   Para obter sua chave de API:
   1. Acesse https://console.groq.com
   2. Faça login ou crie uma conta
   3. Vá para API Keys e gere uma nova chave

4. **Configure as variáveis de ambiente:**

## 🏃‍♂️ Executando o Projeto

```bash
streamlit run src/app.py
```

O aplicativo estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
agente_financeiro/
├── src/
│   └── app.py              # Aplicação principal Streamlit
├── data/
│   ├── transacoes.csv      # Histórico de transações
│   ├── perfil_investidor.json  # Perfil do usuário
│   └── produtos_financeiros.json # Produtos disponíveis
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
└── requirements.txt        # Dependências Python
```

## 🎯 Como Usar

1. **Faça uma pergunta financeira** no campo de texto
2. **O agente analisará** seu perfil, transações e produtos disponíveis
3. **Receba recomendações** personalizadas baseadas no seu contexto

**Exemplos de perguntas:**
- "Como posso otimizar meu orçamento mensal?"
- "Quais investimentos são adequados para meu perfil moderado?"
- "Quanto consigo economizar para comprar um imóvel?"

## 🔧 Dados de Exemplo

O projeto inclui dados de exemplo para demonstração:

- **Perfil:** João Silva, 35 anos, perfil moderado
- **Transações:** Dados de janeiro/2024 com salário e despesas
- **Produtos:** Tesouro Selic, CDB, Ações e Fundos

## ⚠️ Status do Protótipo

**Este é um protótipo em desenvolvimento.**

### Funcionalidades Implementadas:
- ✅ Interface web funcional
- ✅ Integração com API do Groq
- ✅ Análise de dados financeiros
- ✅ Recomendações básicas

### Melhorias Planejadas:
- 🔄 Autenticação de usuários
- 🔄 Banco de dados persistente
- 🔄 Gráficos e visualizações
- 🔄 Histórico de conversas
- 🔄 Integração com APIs bancárias
- 🔄 Validação de dados em tempo real
- 🔄 Testes automatizados
- 🔄 Deploy em produção

## 🐛 Possíveis Problemas

1. **Chave da API inválida:** Verifique se sua chave do Groq está correta e ativa
2. **Módulo groq não encontrado:** Execute `pip install groq`
3. **Caminhos de dados:** Execute o app a partir da pasta raiz do projeto
4. **Conexão com API:** Verifique sua conexão com a internet e se a API do Groq está disponível

