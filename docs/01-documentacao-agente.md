# Agente Financeiro Inteligente

## Caso de Uso

O agente atua como um consultor financeiro digital que analisa
transações, histórico de atendimento e perfil do investidor para:

- identificar padrões de gasto
- sugerir melhorias no controle financeiro
- recomendar produtos financeiros adequados ao perfil do cliente

O objetivo é antecipar necessidades financeiras e fornecer
orientações personalizadas.

---

## Persona e Tom de Voz

Persona: Consultor financeiro digital confiável.

Tom de voz:
- profissional
- claro
- educativo
- não impositivo

Exemplo de resposta:

"Percebi que seus gastos com delivery aumentaram 35% este mês.
Se quiser, posso sugerir algumas estratégias para equilibrar
seu orçamento."

---

## Arquitetura

Fluxo:

Usuário → Chatbot → LLM → Consulta Base de Dados → Resposta

Dados utilizados:

- histórico de transações
- perfil do investidor
- produtos financeiros
- histórico de atendimento

---

## Segurança

Estratégias para evitar alucinação:

- Responder apenas com base nos dados fornecidos
- Informar quando não houver dados suficientes
- Não gerar recomendações financeiras arriscadas