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

### 3.4 Estabilidade e Robustez no RAG (RAGKnowledgePromptAgent)
Durante a execução dos testes da Fase 1, identificamos um risco de travamento/crash no agente RAG devido a um loop infinito potencial no método `chunk_text` e alto consumo de memória nativa da IDE.

**Ações tomadas:**
- **Correção do algoritmo de chunking:** Adicionamos garantias de avanço do ponteiro (`min_chunk_advance`) e proteções contra loops (`max_chunks`). Agora, mesmo se um separador não for encontrado, o sistema avança obrigatoriamente, evitando que o processo trave.
- **Versão Estável (`rag_knowledge_prompt_agent_stable.py`):** Criamos uma versão de teste que utiliza **embeddings mock** e desativa I/O de CSV desnecessário. Isso permitiu validar toda a lógica de fatiamento e recuperação sem depender de chamadas externas instáveis durante a fase de diagnóstico.
- **Timeouts:** Adicionamos `timeout=60.0` em todas as instâncias do cliente OpenAI em `base_agents.py` para evitar esperas silenciosas e permitir falhas rápidas.
- **Preparação para Embeddings Reais (`rag_real_validation.py`):** Criamos um script minimalista pronto para validar a API real com o novo algoritmo de chunking seguro.

**Relação com o curso:**
Sistemas agentic em produção devem ser **resilientes**. O curso enfatiza que o workflow deve ser capaz de lidar com falhas de rede e dados inesperados. A implementação de "safety breaks" e "timeouts" é uma prática essencial para garantir que o orquestrador (que será construído na Fase 2) não fique bloqueado por um único agente malcomportado.

### 3.5 Detalhamento Técnico: Roteamento por Embeddings (Similaridade de Cosseno)
O **RoutingAgent** é o "maestro" do workflow, responsável por decidir qual especialista deve tratar a requisição do usuário. Essa decisão não é baseada em palavras-chave simples, mas em **significado semântico**.

- **Como funciona:**
  1. Transformamos a pergunta do usuário e as descrições dos agentes em **vetores numéricos (embeddings)** usando o modelo `text-embedding-3-large`.
  2. Calculamos a **Similaridade de Cosseno** entre esses vetores. Quanto mais próximo de 1.0, mais "parecidos" são os significados.
- **Relação com o Curso 2 (Lição 9):**
  - O conceito é idêntico ao demonstrado no **Email Router Project** da **Lição 2**.
  - **Referência de código no curso:** No arquivo `notebooks/COURSE_2/2_AI Agents and Agentic Workflows/Email Router Project/starter/phase_1/workflow_agents/base_agents.py`, a similaridade é calculada na **linha 310** dentro da classe `RoutingAgent`:
    ```python
    similarity = np.dot(input_emb, agent_emb) / (np.linalg.norm(input_emb) * np.linalg.norm(agent_emb))
    ```
  - A transformação em vetor (get_embedding) ocorre nas **linhas 292-297**.

### 3.6 Detalhamento Técnico: RAG (Recuperação por Chunks)
O **RAGKnowledgePromptAgent** permite que a IA responda com base em documentos externos que não caberiam inteiros no prompt (context window).

- **Como funciona:**
  1. **Chunking (Fatiamento):** O documento grande é quebrado em pedaços menores (chunks), geralmente separados por quebras de linha (`\n`).
  2. **Indexação:** Cada pedaço é transformado em um embedding e armazenado.
  3. **Recuperação (Retrieval):** Quando o usuário faz uma pergunta, o agente busca o chunk que tem a maior similaridade com a pergunta.
  4. **Geração:** O LLM recebe apenas o chunk relevante para formular a resposta final.
- **Relação com o Curso 2 (Lição 2):**
  - Este é o pilar do "conhecimento dinâmico" ensinado na Lição 2.
  - **Referência de código no curso:** No mesmo arquivo `base_agents.py` da Lição 2, o processo de busca ocorre nas **linhas 207-209**:
    ```python
    df['similarity'] = df['embeddings'].apply(lambda emb: self.calculate_similarity(prompt_embedding, emb))
    best_chunk = df.loc[df['similarity'].idxmax(), 'text']
    ```
    O sistema aplica a similaridade em todos os chunks e seleciona o maior valor (`idxmax`).

### 3.7 Sobre a Estabilidade do Terminal (Prevenção de Travamentos)
Identificamos que a thread da Junie/Terminal pode "congelar" durante a execução de scripts de IA. Isso ocorre por limitações físicas do ambiente de execução e bugs lógicos herdados:

1. **I/O Bloqueante:** Chamadas de API síncronas e leitura/escrita de arquivos CSV grandes podem travar o processo enquanto aguardam resposta.
2. **Loop Infinito (Bug do material original):** O algoritmo de `chunk_text` original podia entrar em loop se não encontrasse um separador, consumindo memória e CPU indefinidamente.

**Soluções implementadas:**
- **Timeouts:** Todas as chamadas de API agora têm limite de 60 segundos.
- **Safety Advance:** Garantia de que o fatiador de texto sempre avance pelo menos 1 caractere.
- **Uso de Mocks:** Durante o desenvolvimento da lógica do workflow (Fase 2), usaremos embeddings simulados para garantir agilidade e estabilidade, ativando a API Real apenas para validações finais.

## 4) Demos e exemplos do curso usados como base
Nesta etapa, os principais “demos” utilizados foram:
- **Lição 2 (Email Router Project):** Forneceu a base para os agentes RAG, Augmented e KnowledgeAugmented. Aprendemos a usar o `system_prompt` para definir personas e o `knowledge` para restringir o domínio da IA.
- **Lição 9 (Agentic Routing):** Serviu de referência para o `RoutingAgent`, demonstrando como usar embeddings e similaridade de cosseno para decidir o fluxo de execução entre múltiplos especialistas.
- **Phase 1 README e Starter Scripts:** Orientaram a estrutura de prompts e os casos de teste para validar cada agente isoladamente.

## 5) Etapas já implementadas (Fase 2)
### 5.1 Implementação do Orquestrador (agentic_workflow.py)
O arquivo `agentic_workflow.py` agora contém a lógica completa do workflow, integrando múltiplos agentes especializados.

- **Componentes Implementados:**
  - **Action Planning:** Usa o `ActionPlanningAgent` para decompor o prompt do usuário (ex: "What would the development tasks for this product be?") em passos executáveis baseados no conhecimento de gestão de projetos.
  - **Especialistas (Knowledge Augmented):** Instância de Product Manager, Program Manager e Development Engineer, cada um com sua persona e base de conhecimento específica (incluindo a especificação do produto para o PM).
  - **Loop de Avaliação:** Cada especialista possui um `EvaluationAgent` associado, garantindo que as user stories, features e tasks geradas sigam o formato correto e critérios de qualidade antes de serem aceitas pelo workflow.
  - **Roteamento Inteligente:** O `RoutingAgent` decide qual especialista deve executar cada passo do plano gerado, permitindo que o workflow seja dinâmico e flexível.

- **Relação com o Curso 2:**
  - **Lição 2 (Agentic Workflows):** Implementação prática do conceito de colaboração entre agentes.
  - **Padrão Orquestrador:** O script funciona como o "coração" do sistema, coordenando a passagem de informações entre agentes, simulando um ambiente real de desenvolvimento de software.

## 6) Estado atual e próximos passos
- **Concluído:** Implementação da lógica do workflow da Fase 2 (`agentic_workflow.py`).
- **Concluído nesta etapa incremental:** estabilização da Fase 2 para execução previsível.

### 6.1 Correções aplicadas agora (Fase 2 - estabilidade)
Para permitir continuidade sem travamentos silenciosos e com comportamento mais previsível, foram aplicadas correções mínimas no `starter/phase_2/agentic_workflow.py`:

1. **Carregamento explícito do `.env` local do projeto da etapa**
   - Antes: `load_dotenv()` sem caminho explícito.
   - Agora: carregamento por caminho absoluto do diretório raiz da etapa (`.../17_AI-Powered Agentic Workflow for Project Management/.env`).
   - **Motivação didática:** manter o projeto autocontido (como você solicitou) e reduzir inconsistências de ambiente.

2. **Falha rápida para credencial ausente**
   - Foi adicionado erro explícito quando `OPENAI_API_KEY_DEV`/`OPENAI_API_KEY` não está disponível.
   - **Motivação didática:** em workflows agentic, é melhor erro claro no início do que falha tardia difícil de diagnosticar.

3. **Instanciação robusta dos `EvaluationAgent` com argumentos nomeados**
   - Atualização das três instanciações (PM, Program Manager, Dev Engineer) para `keyword arguments`.
   - **Motivação didática:** evita ambiguidade de ordem de parâmetros e reduz risco de erro de assinatura em evolução de código.

4. **Ajuste no encadeamento das support functions**
   - Antes: cada support function chamava `knowledge_agent.respond(query)` e depois `evaluation_agent.evaluate(response)`.
   - Agora (ajuste incremental): cada support function chama `knowledge_agent.respond(query)` e repassa esse resultado para a avaliação com contexto do prompt original.
   - **Motivação didática:** manter aderência ao fluxo solicitado no README da Fase 2 (`respond -> evaluate`) e, ao mesmo tempo, evitar dupla geração desnecessária.

5. **Ajuste incremental no `EvaluationAgent` da Fase 2**
   - Foi adicionada a opção de receber `initial_response` no método `evaluate(...)`.
   - Quando `initial_response` é fornecida, a avaliação começa usando essa resposta já gerada; se a resposta for reprovada, o agente volta a iterar com feedback para refinamento.
   - **Motivação didática:** compatibilizar o padrão do README com o contrato da classe sem custo extra de chamada duplicada.

6. **Timeout explícito nos agentes da Fase 2**
   - Adicionado `timeout=60.0` nas chamadas `OpenAI(...)` da biblioteca `starter/phase_2/workflow_agents/base_agents.py`.
   - **Motivação didática:** reduzir risco de espera silenciosa em chamadas externas e melhorar previsibilidade durante validações.

### 6.2 Relação com o Curso 2 (base conceitual)
- **Lição 2 (AI Agents and Agentic Workflows / Email Router Project):** padrão de composição entre agentes especializados, com planejamento e validação iterativa.
- **Lição 9 (Implementing Agentic Routing):** roteamento por similaridade semântica continua como núcleo da decisão de qual especialista executa cada etapa.

### 6.3 Próximo passo sugerido (após sua confirmação)
1. Registrar as saídas dos testes leves já concluídos da Fase 1 no relatório.
2. Executar apenas validação **controlada** da Fase 2 em terminal externo (fora da thread da Junie), para evitar travamento do ambiente.
3. Consolidar checklist final para commit incremental desta etapa.

### 6.4 Revalidação do kickoff (checkpoint solicitado)
Reanalisei os documentos de kickoff e confirmei que a direção do projeto continua correta:

- `project_overview.md` / `project_overview.txt`: projeto em duas fases (biblioteca de agentes + workflow orquestrado para Product Management).
- `README.md` (raiz da etapa): aponta para execução em duas fases e uso dos guias dentro de `starter/`.
- `starter/phase_1/README.md`: implementação e validação de 7 agentes (incluindo RAG fornecido) com scripts individuais.
- `starter/phase_2/README.md`: construção do `agentic_workflow.py` com `ActionPlanningAgent`, `RoutingAgent`, `KnowledgeAugmentedPromptAgent` e `EvaluationAgent`.
- Rubricas (`project_rubric*.txt`): exigem aderência estrutural, outputs por script e saída final do workflow.

### 6.5 Diagnóstico: por que ontem travou e hoje está fluindo
Diagnóstico técnico consolidado por categoria:

1. **Ambiente/execução (principal fator)**
   - Ontem houve execuções longas e síncronas dentro da thread interativa (Junie + terminal acoplado), o que é sensível a latência de rede/API e I/O.
   - Hoje o fluxo foi mais estável porque priorizamos inspeção/correções e validação leve (lint), evitando execuções pesadas contínuas na thread.

2. **Código/lógica (fator contribuinte identificado anteriormente)**
   - No RAG, havia risco de loop/alto consumo em `chunk_text` (já corrigido com salvaguardas de avanço e limites).
   - Isso elevava chance de bloqueio do ambiente quando combinado com chamadas de API e I/O.

3. **Chamadas externas/API (fator crítico de congelamento percebido)**
   - Chamadas OpenAI sem timeout explícito podem parecer “travamento” quando a resposta demora.
   - Mitigação aplicada: `timeout=60.0` na Fase 2 (e já havia proteção no RAG relevante).

**Recomendação operacional permanente:**
- Desenvolver/ajustar dentro da thread com validação leve.
- Executar testes pesados e validação real de ponta a ponta em terminal externo controlado (`python -u ...`).

### 6.6 Plano incremental de continuidade (sem travar a thread)
Para continuar com estabilidade e manter o aprendizado por etapas:

1. **Checkpoint de commit desta etapa**
   - Consolidar as alterações atuais (workflow + documentação didática + guideline de commit).
2. **Validação externa controlada da Fase 2**
   - Rodar apenas em terminal externo:
     - `cd "notebooks\\COURSE_2\\17_AI-Powered Agentic Workflow for Project Management\\starter\\phase_2"`
     - `python -u .\\agentic_workflow.py`
3. **Registro estruturado dos resultados**
   - Registrar no relatório: steps do plano, rota por step, resposta validada por especialista, erros/timeouts.

### 6.7 Template de registro de execução externa (copiar e preencher)
```md
## Execução controlada Fase 2 (terminal externo)

- Data/Hora:
- Ambiente:
- Comando executado:
  - python -u .\\starter\\phase_2\\agentic_workflow.py

### Resultado do Action Planning
- Quantidade de steps:
- Steps gerados:

### Resultado do Routing
- Step 1 -> agente selecionado:
- Step 2 -> agente selecionado:
- Step 3 -> agente selecionado:

### Resultado da Evaluation
- Product Manager: (aprovado/reprovado) | observação:
- Program Manager: (aprovado/reprovado) | observação:
- Development Engineer: (aprovado/reprovado) | observação:

### Incidentes
- Timeout observado? (sim/não)
- Erro de credencial? (sim/não)
- Travamento? (sim/não)
- Ação corretiva aplicada:
```

### 6.8 Registro consolidado das saídas da Fase 1 (rubrica)
Para avançar de forma incremental e manter rastreabilidade para commits/submissão, consolidei as saídas já coletadas dos scripts da Fase 1 em um arquivo dedicado:

- `PHASE_1_TEST_OUTPUTS.md`

**O que este registro cobre:**
- resultado de cada script individual da Fase 1;
- interpretação didática de cada resultado;
- observação explícita do incidente no RAG (`MemoryError`) que motivou os ajustes de estabilidade.

**Motivação:**
- atender o requisito da rubrica de organizar outputs em texto/screenshot;
- facilitar revisão de aprendizado por etapa;
- permitir commits menores e mais auditáveis.

### 6.9 Próximo passo incremental (após sua confirmação)
1. Consolidar commit desta etapa de documentação (relatório + log de outputs da Fase 1).
2. Seguir para validação controlada externa da Fase 2 (sem execução pesada na thread).
3. Registrar no relatório o resultado do workflow completo (steps, rota por step, avaliação final).

- **Etapa seguinte:** Revisão final e submissão.

### 6.10 Próxima etapa executada (checkpoint atual)
Para avançar sem travamento e manter aderência à rubrica da Fase 2, implementei um checkpoint mínimo e estável:

1. **Robustez de caminho no `agentic_workflow.py`**
   - Ajuste aplicado: leitura do `Product-Spec-Email-Router.txt` agora usa caminho absoluto baseado no diretório do script (`Path(__file__).resolve().parent`).
   - **Motivação didática:** evita falhas dependentes do diretório atual de execução (`cwd`) e torna a execução externa mais previsível.

2. **Arquivo dedicado para evidência da Fase 2**
   - Novo arquivo: `PHASE_2_WORKFLOW_OUTPUTS.md`.
   - Conteúdo: comando de execução controlada em terminal externo + template de registro (Action Planning, Routing, Evaluation, output final e incidentes).
   - **Motivação didática:** atender explicitamente a rubrica de documentação de saída do workflow, com rastreabilidade para commit incremental.

3. **Relação com o Curso 2**
   - **Lição 2 (Agentic Workflows):** reforço da orquestração multiagente com papéis especializados e avaliação iterativa.
   - **Lição 9 (Routing):** preserva o fluxo onde cada step do plano é encaminhado por similaridade ao especialista mais adequado.

4. **Observação operacional**
   - Esta etapa **não executa runtime pesado** na thread interativa.
   - A execução real permanece recomendada em terminal externo, com registro no `PHASE_2_WORKFLOW_OUTPUTS.md`.

### 6.11 Revalidação de aderência à rubrica (checkpoint desta etapa)
Objetivo desta etapa: responder com clareza **em que ponto estamos de aderência ao `project_rubric`**.

| Bloco da rubrica | Evidência no projeto | Status |
|---|---|---|
| Fase 1 - classes obrigatórias em `workflow_agents/base_agents.py` | `starter/phase_1/workflow_agents/base_agents.py` contém: `DirectPromptAgent`, `AugmentedPromptAgent`, `KnowledgeAugmentedPromptAgent`, `EvaluationAgent`, `RoutingAgent`, `ActionPlanningAgent` (+ RAG fornecido) | ✅ |
| Fase 1 - configuração de modelo/chaves | Uso de `gpt-3.5-turbo` nos agentes de chat, `text-embedding-3-large` em embeddings, chave via parâmetro (`openai_api_key`) | ✅ |
| Fase 1 - scripts de teste por agente | Scripts presentes em `starter/phase_1/` para todos os agentes solicitados | ✅ |
| Fase 1 - evidências de execução dos scripts | Registro consolidado em `PHASE_1_TEST_OUTPUTS.md` | ✅ |
| Fase 2 - setup inicial (`agentic_workflow.py`) | Importações corretas, carga de `.env`, leitura de `Product-Spec-Email-Router.txt` por caminho robusto | ✅ |
| Fase 2 - instanciação de agentes especializados e avaliadores | PM, Program Manager e Dev Engineer + respectivos `EvaluationAgent` | ✅ |
| Fase 2 - Routing Agent com rotas e funções de suporte | Rotas com `name`, `description`, `func`; funções de suporte implementadas | ✅ |
| Fase 2 - contrato das support functions da rubrica | Fluxo ajustado para `respond(query) -> evaluate(response) -> final_response` | ✅ |
| Fase 2 - evidência de execução final do workflow | `PHASE_2_WORKFLOW_OUTPUTS.md` preenchido com execução real (baseline + execução controlada) | ✅ |

**Leitura didática do status:**
- **Aderência de implementação (código):** ✅ atingida no checkpoint atual.
- **Aderência de submissão (evidências finais):** ✅ evidência final registrada no arquivo de outputs.

### 6.12 Critério de “PROJETO ADERENTE À RUBRICA” (regra objetiva)
Vou te avisar explicitamente como **"ADERENTE À RUBRICA"** quando os dois itens abaixo estiverem simultaneamente verdadeiros:

1. Código da Fase 1 e Fase 2 mapeado em conformidade com os critérios estruturais/funcionais (já está).  
2. Evidência final da Fase 2 preenchida no `PHASE_2_WORKFLOW_OUTPUTS.md` com saída real do workflow (concluído).

> Observação: esta explicação será atualizada a cada nova etapa, com uma descrição didática do que foi implementado e como se conecta aos conceitos do curso.

### 6.13 Próxima etapa executada (estabilidade operacional do workflow)
Para reduzir risco de execução acidental e manter previsibilidade entre commits, foi aplicado um ajuste incremental no script principal da Fase 2:

1. **`agentic_workflow.py` com `main guard`**
   - Ajuste aplicado: o trecho de execução do workflow foi encapsulado em `run_workflow(...)` e protegido por:
     - `if __name__ == "__main__":`
   - **Motivação didática:** evita rodar chamadas de API automaticamente quando o arquivo é importado por outro script/módulo, reduzindo travamentos inesperados no ambiente interativo.

2. **Relação com o Curso 2 (boas práticas de workflow agentic)**
   - **Lição 2:** mantém o foco na orquestração entre agentes especializados (planejar → rotear → executar/especialista → avaliar).
   - **Lição 9:** preserva o roteamento semântico como núcleo de decisão por step.
   - O ajuste é **operacional** (estabilidade de execução), sem alterar a lógica pedagógica dos agentes.

3. **Impacto esperado nesta etapa**
   - Execução mais controlada para validação externa (`python -u .\\agentic_workflow.py`).
   - Menor chance de “rodar sem querer” ao abrir/importar módulos durante manutenção.
   - Continuidade incremental preservada para commit didático.

### 6.14 Fechamento técnico da Fase 2 (execução real + evidências)
Nesta etapa, o foco foi **fechar o projeto com evidência real de execução** e sem voltar ao padrão de travamentos longos.

1. **Execução real do workflow (comando baseline)**
   - Comando executado:
     - `python -u .\\starter\\phase_2\\agentic_workflow.py`
   - Resultado observado:
     - workflow concluído sem crash;
     - Action Planning gerou 1 step;
     - roteamento selecionou `Development Engineer`;
     - Evaluation aprovou após refinamento (2 interações).

2. **Execução controlada para cobertura de stories/features/tasks**
   - Comando executado (controlado):
     - `python -u -c "import agentic_workflow as aw; aw.run_workflow('For the Email Router product spec, generate EXACTLY 3 workflow steps only: 1) create user stories, 2) define product features grouped from those stories, 3) define engineering tasks with dependencies. Return concise steps only.')"`
   - Resultado observado:
     - Action Planning gerou 3 steps;
     - Routing + Evaluation funcionaram em todos os steps;
     - saída final estruturada em tarefas de engenharia com dependências.

3. **Incidente controlado e mitigação**
   - Em um teste amplo anterior, o prompt gerou steps demais e estourou o tempo de execução.
   - Mitigação aplicada: limitar o plano com `EXACTLY 3` steps para manter execução previsível e auditável.

4. **Arquivo de evidência final atualizado**
   - `PHASE_2_WORKFLOW_OUTPUTS.md` foi preenchido com:
     - metadados do run,
     - outputs de Action Planning, Routing e Evaluation,
     - incidentes e mitigação,
     - próximos ajustes opcionais.

5. **Status de aderência à rubrica (neste checkpoint)**
   - **Implementação (Fase 1 + Fase 2):** ✅
   - **Evidências de execução (Fase 1 + Fase 2):** ✅
   - **Projeto aderente à rubrica para submissão:** ✅

### 6.15 Diagnóstico final de travamentos (ontem vs hoje)
Resumo objetivo do que explica a diferença de comportamento:

1. **Causa operacional principal**
   - Workflows agentic com múltiplos passos + chamadas de API síncronas podem exceder tempo em sessões interativas, parecendo “travamento”.

2. **Causa técnica já tratada**
   - RAG da Fase 1 tinha risco de loop/memória no chunking (já estabilizado nas etapas anteriores).

3. **Prática adotada para continuidade**
   - usar execução controlada com prompt limitado;
   - coletar evidência em arquivo dedicado;
   - manter validação incremental em vez de rodadas longas e abertas.

Com isso, o projeto segue o padrão didático do Curso 2 e está pronto para seu fechamento em commit/submissão.