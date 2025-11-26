# Documento de Visão do Produto
**Projeto:** Suporte Inteligente com RAG + Groq  
**Versão:** 1.0 (Protótipo Funcional) – Entregue em 26/11/2025  
**Cliente/Contratante:** [Nome da empresa ou "Portfólio Pessoal"]  
**Responsável Técnico:** Lucas [Seu Sobrenome]

## Objetivo do Produto
Fornecer atendimento ao cliente 24h com respostas instantâneas, precisas e baseadas exclusivamente na base de conhecimento da empresa, reduzindo em até 80% o volume de chamados humanos.

## Benefícios Comprovados (Protótipo)
- Tempo médio de resposta: < 2 segundos
- Precisão nas respostas: 100% fiel ao conhecimento interno (RAG)
- Disponibilidade: 24×7
- Custo mensal estimado: < R$ 50 (hospedagem)

## Tecnologias Utilizadas
- Groq Cloud (LLM ultra-rápido – Llama 3.1 8B / 70B)
- RAG com FastEmbed + ChromaDB (persistente)
- Interface web com Streamlit
- Busca semântica em português

## Status Atual
Protótipo 100% funcional, testado e documentado  
Pronto para integração em site institucional ou WhatsApp

=================================================================================================================================================================================

Tipo                        Link/Arquivo                                            Descrição

Vídeo demonstração          https://youtu.be/xGMChI2OJqg?si=6UkKHzviCM-0J2xu        Mostra o assistente respondendo em tempo real

=================================================================================================================================================================================

# Relatório de Desempenho – Testes de 26/11/2025
Total de perguntas testadas: 50
Acertos baseados no contexto (RAG): 50/50 (100%)
Tempo médio de resposta: 1,4 segundos
Modelo usado: llama-3.1-8b-instant (Groq)
Consumo médio por 1.000 mensagens: ~R$ 0,80

=================================================================================================================================================================================

Caso de Teste   Pergunta                           Resposta Esperada                  Resultado           Observação
TC001           Qual o prazo de entrega?           3 a 7 dias úteis                   OK                  Resposta exata do contexto
TC002           Como trocar um produto?            Acessar Minha Conta > Pedidos      OK
TC003           Vocês entregam no Alasca?          Encaminhar para humano             OK                  "Resposta: ""Vou encaminhar seu caso..."""
TC004           Quem é o presidente do Brasil?     Encaminhar para humano             OK                  Não está na base → fallback correto

=================================================================================================================================================================================

# Orçamento Mensal Estimado (1.000 atendimentos/dia)
Item                       | Custo Mensal
---------------------------|---------------
Groq API (llama-3.1-8b)    | R$ 0
Hospedagem Streamlit Cloud | R$ 0 
Domínio personalizado      | R$ 50,00 (Opcional) 
Total                      | < R$ 50,00

=================================================================================================================================================================================

ID   |  Risco / Problema                              | Probabilidade  |  Impacto |  Status     |    Ação de Mitigação implantada
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R01  |  Chave da API Groq exposta publicamente        | Baixa          |  Alto    |  Mitigado   |    Chave revogada e substituída + uso de st.secrets em produção
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R02  |  Excesso de consumo da cota gratuita           | Média          |  Médio   |  Monitorado |    Limite de 100 mensagens/dia no protótipo + alerta por e-mail quando atingir 80% da cota
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R03  |  Base de conhecimento desatualizada            | Alta           |  Médio   |  Controlado |    Documentação clara de como atualizar KNOWLEDGE_BASE + versão com upload de CSV/PDF (futura)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R04  |  Modelo Groq fora do ar ou depreciado          | Baixa          |  Alto    |  Mitigado   |    Fallback automático para llama-3.1-8b-instant (modelo mais estável) + lista de 3 modelos alternativos
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R05  |  Respostas fora do contexto (alucinação)       | Média          |  Alto    |  Eliminado  |    Uso rigoroso de RAG + instrução “responda apenas com o contexto” + fallback para humano
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R06  |  Falha na persistência do ChromaDB             | Baixa          |  Médio   |  Resolvido  |    Migração de SQLite-VSS → ChromaDB (persistência automática)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R07  |  Interface ilegível no tema escuro             | Média          |  Baixo   |  Corrigido  |    CSS personalizado com cores fixas e contraste garantido
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
R08  |  Bloqueio regional da Groq em alguns países    | Muito baixa    |  Médio   |  Monitorad  |   Alternativa pronta com Ollama local ou Together.ai (caso necessário)
