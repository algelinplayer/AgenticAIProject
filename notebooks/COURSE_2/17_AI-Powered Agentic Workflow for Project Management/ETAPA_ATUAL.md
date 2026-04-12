# Relatório Didático — AI-Powered Agentic Workflow for Project Management

## 1) O que é este projeto
Este projeto implementa um **workflow agentic** para gestão de desenvolvimento de produto. A ideia central é usar agentes especializados (Product Manager, Program Manager e Development Engineer) para transformar uma **especificação de produto** em **user stories**, **features** e **tarefas de engenharia**. Essa arquitetura segue o objetivo do curso: criar sistemas de IA que **planejam, roteiam e avaliam** suas próprias saídas, em vez de um fluxo rígido e estático.

## 2) Plano de trabalho (alto nível)
1. **Fase 1 — Biblioteca de Agentes:** implementar agentes reutilizáveis (base_agents.py) e seus scripts de teste.  
2. **Fase 1 — Validação:** executar os scripts e coletar saídas.  
3. **Fase 2 — Workflow:** montar o orquestrador (agentic_workflow.py) com Action Planning, Routing, Knowledge Agents e Evaluation Agents.  
4. **Fase 2 — Validação:** rodar o workflow com o Product-Spec-Email-Router e capturar resultados.  

## 3) Etapas já implementadas (Fase 1)
### 3.1 Biblioteca de agentes (workflow_agents/base_agents.py)
Implementação dos agentes conforme as instruções do **Phase 1 README** e a rubrica:

- **DirectPromptAgent**
  - **Motivação:** representar o caso base de interação direta com LLM (sem contexto adicional).  
  - **Relação com o curso:** demonstra o “prompt direto” como baseline de agentes.

- **AugmentedPromptAgent**
  - **Motivação:** incorporar persona como **system prompt**, alterando o comportamento do agente.  
  - **Relação com o curso:** evidencia o papel de “persona” e “system messages” para direcionar respostas.

- **KnowledgeAugmentedPromptAgent**
  - **Motivação:** restringir respostas a um bloco de conhecimento fornecido, simulando conhecimento especializado.  
  - **Relação com o curso:** ilustra controle de contexto e grounding explícito.

- **RAGKnowledgePromptAgent (fornecido)**
  - **Motivação:** demonstrar uso de embeddings + recuperação de conhecimento.  
  - **Relação com o curso:** conecta com a ideia de RAG em workflows agentic.

- **EvaluationAgent**
  - **Motivação:** implementar o loop **worker → evaluator → correção**, garantindo aderência a critérios.  
  - **Relação com o curso:** reforça o padrão “self-critique / evaluator loop”, essencial em sistemas agentic.

- **RoutingAgent**
  - **Motivação:** selecionar o melhor agente especialista com base em similaridade semântica (embeddings).  
  - **Relação com o curso:** corresponde ao padrão de **roteamento inteligente** em workflows.

- **ActionPlanningAgent**
  - **Motivação:** extrair passos de uma tarefa usando conhecimento fornecido.  
  - **Relação com o curso:** é o módulo de **planejamento**, que decompõe metas em etapas.

### 3.2 Scripts de teste da Fase 1
Foram mantidos/ajustados os scripts de teste individuais de cada agente, seguindo o padrão do **Phase 1 README**:

- direct_prompt_agent.py  
- augmented_prompt_agent.py  
- knowledge_augmented_prompt_agent.py  
- rag_knowledge_prompt_agent.py  
- evaluation_agent.py  
- routing_agent.py  
- action_planning_agent.py  

**Motivação:** validar o comportamento de cada agente isoladamente antes de compor o workflow da Fase 2.

### 3.3 Padronização do Model Provider Key (Vocareum)
Para manter consistência com os **demos e exercícios do Curso 2**, os clientes OpenAI passaram a usar:

- `base_url = "https://openai.vocareum.com/v1"` (padrão observado nos demos).  
- `OPENAI_API_KEY_DEV` como variável principal de autenticação (com fallback para `OPENAI_API_KEY`).  

**Motivação:** garantir compatibilidade com a infraestrutura do curso e evitar erros de autenticação ao executar os scripts de teste.

## 4) Demos e exemplos do curso usados como base
Nesta etapa, os principais “demos” utilizados foram os próprios **scripts de teste e README da Phase 1** (notebooks/COURSE_2/17_AI-Powered Agentic Workflow for Project Management/starter/phase_1), que explicitam padrões de implementação e testes para cada agente. Esses exemplos orientam:

- Estrutura de prompts (system vs user).  
- Uso de persona e conhecimento específico.  
- Loop de avaliação e correção.  
- Roteamento por embeddings.  
- Planejamento de ações baseado em conhecimento.  

Esse conjunto de exemplos consolida o conteúdo do Curso 2 sobre **agentic workflows**, especialmente os blocos de **planejamento**, **roteamento**, **avaliação**, e **agentes especializados**.

## 5) Estado atual e próximos passos
- **Concluído:** Implementação da Fase 1 (biblioteca + scripts).  
- **Próximo passo sugerido:** executar os testes da Fase 1 e registrar saídas.  
- **Etapa seguinte:** implementar o workflow da Fase 2 em agentic_workflow.py.  

> Observação: esta explicação será atualizada a cada nova etapa, com uma descrição didática do que foi implementado e como se conecta aos conceitos do curso.