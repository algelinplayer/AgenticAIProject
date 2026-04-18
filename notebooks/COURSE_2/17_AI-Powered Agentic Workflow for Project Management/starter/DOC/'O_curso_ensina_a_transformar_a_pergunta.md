### Esclarecimento sobre Localização do Conteúdo e Travamento

É fundamental alinhar o código que estamos desenvolvendo com os exemplos exatos do curso para garantir que você esteja aprendendo o padrão correto. Abaixo, aponto as referências solicitadas e explico como lidar com a instabilidade do terminal.

### 1. Roteamento por Embeddings (Similaridade de Cosseno)
O curso ensina a transformar a pergunta e as descrições em vetores para calcular a similaridade no **Email Router Project** da **Lição 2**. Embora a Lição 9 também trate de roteamento, o exemplo base para o uso de **Embeddings** e **Numpy** está no arquivo de estrutura da Lição 2.

*   **Localização:** `notebooks/COURSE_2/2_AI Agents and Agentic Workflows/Email Router Project/starter/phase_1/workflow_agents/base_agents.py`
*   **Linha do Cálculo (Similaridade de Cosseno):** Linha **310** (dentro da classe `RoutingAgent`):
    ```python
    similarity = np.dot(input_emb, agent_emb) / (np.linalg.norm(input_emb) * np.linalg.norm(agent_emb))
    ```
*   **Linha da Transformação em Vetor:** Linhas **292-297** (método `get_embedding`).

### 2. RAG (Recuperação por Chunks)
O uso de embeddings para vasculhar documentos (RAG) também é introduzido no **Email Router Project** da **Lição 2**, sendo o pilar do agente de conhecimento.

*   **Localização:** `notebooks/COURSE_2/2_AI Agents and Agentic Workflows/Email Router Project/starter/phase_1/workflow_agents/base_agents.py`
*   **Linha do Processo de Busca:** Linhas **207-209** (dentro de `find_prompt_in_knowledge`):
    ```python
    df['similarity'] = df['embeddings'].apply(lambda emb: self.calculate_similarity(prompt_embedding, emb))
    best_chunk = df.loc[df['similarity'].idxmax(), 'text']
    ```
    Aqui, o código aplica a similaridade em todos os parágrafos (chunks) e seleciona o que tiver o maior valor (`idxmax`).

---

### 3. Sobre o Travamento da Junie/Terminal

**Por que trava?**
O travamento **não é um problema do Modelo de IA** (o cérebro), mas sim da **Execução do Script** (o corpo). Ocorre por dois motivos técnicos:
1.  **I/O Bloqueante:** Scripts de teste originais tentam ler/escrever arquivos CSV e fazer chamadas de API síncronas. Se a API demora ou o arquivo é grande, a thread do terminal da IDE fica "congelada" aguardando a resposta.
2.  **Loop Infinito (Bug Original):** O algoritmo de `chunk_text` fornecido no material inicial tinha um risco lógico: se ele não encontrasse um `\n` perto do limite, o ponteiro de início não avançava, fazendo o script rodar para sempre e consumir toda a memória.

**O que você deve fazer?**
Não é necessário mudar o modelo de IA. A solução é de engenharia de software:
1.  **Não execute scripts pesados no terminal interativo:** Para testes reais com a API da OpenAI, prefira usar o comando de execução em segundo plano ou o script de validação mínima que criamos.
2.  **Use a versão estável:** Continue usando as correções que implementamos no `base_agents.py` (com `timeout=60.0` e `min_chunk_advance`). Elas evitam que o script fique preso.
3.  **Use Mocks para Desenvolvimento:** Durante a construção da Fase 2, use o modo `mock` (embeddings simulados) para validar a lógica do workflow. Ative o "Real" apenas para o teste final de integração.

**Próximo Passo:**
Deseja que eu mostre como rodar o script de RAG Real de forma controlada (apenas um trecho pequeno) para você ver o resultado sem travar o seu ambiente?