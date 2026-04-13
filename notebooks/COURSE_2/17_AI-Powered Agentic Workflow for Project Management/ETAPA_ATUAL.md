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
   - Agora: chama diretamente `evaluation_agent.evaluate(query)`, deixando o loop interno do evaluator controlar o worker.
   - **Motivação didática:** evita duplicidade de chamadas ao worker e segue melhor o padrão Worker↔Evaluator do curso.

### 6.2 Relação com o Curso 2 (base conceitual)
- **Lição 2 (AI Agents and Agentic Workflows / Email Router Project):** padrão de composição entre agentes especializados, com planejamento e validação iterativa.
- **Lição 9 (Implementing Agentic Routing):** roteamento por similaridade semântica continua como núcleo da decisão de qual especialista executa cada etapa.

### 6.3 Próximo passo sugerido (após sua confirmação)
1. Registrar as saídas dos testes leves já concluídos da Fase 1 no relatório.
2. Executar apenas validação **controlada** da Fase 2 em terminal externo (fora da thread da Junie), para evitar travamento do ambiente.
3. Consolidar checklist final para commit incremental desta etapa.

- **Etapa seguinte:** Revisão final e submissão.

> Observação: esta explicação será atualizada a cada nova etapa, com uma descrição didática do que foi implementado e como se conecta aos conceitos do curso.