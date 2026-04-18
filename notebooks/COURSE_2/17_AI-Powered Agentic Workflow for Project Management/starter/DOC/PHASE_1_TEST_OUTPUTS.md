# Phase 1 — Test Outputs Log (Consolidated)

This file consolidates the outputs already collected from Phase 1 scripts, organized in text format, as required by the project rubric.

## Environment Context
- Project path: `notebooks/COURSE_2/17_AI-Powered Agentic Workflow for Project Management`
- API key source: local `.env` from project folder (Vocareum provider pattern)
- Execution strategy used: incremental script-by-script validation

## Script Results

1. `starter/phase_1/direct_prompt_agent_standalone_test.py`
   - Result: answered **"The capital of France is Paris."**
   - Interpretation: baseline behavior from general LLM knowledge.

2. `starter/phase_1/augmented_prompt_agent_standalone_test.py`
   - Result: answered politely and addressed students, still giving **Paris** as capital.
   - Interpretation: persona conditioning works as expected.

3. `starter/phase_1/knowledge_augmented_prompt_agent_standalone_test.py`
   - Result: answered **"The capital of France is London, not Paris"**.
   - Interpretation: response was grounded in provided knowledge, not in general model priors.

4. `starter/phase_1/evaluation_agent_standalone_test.py`
   - Result: evaluator rejected sentence format in first pass and accepted corrected output **"London"** in second pass.
   - Interpretation: worker-evaluator refinement loop is functioning.

5. `starter/phase_1/routing_agent_standalone_test.py`
   - Result: selected the most relevant specialist route per prompt (Texas, Europe, Math) with similarity scores and domain-specific answers.
   - Interpretation: semantic routing by embeddings is functioning.

6. `starter/phase_1/action_planning_agent_standalone_test.py`
   - Result: generated a structured step-by-step plan (scrambled eggs example).
   - Interpretation: task decomposition/planning behavior is functioning.

7. `starter/phase_1/rag_knowledge_prompt_agent_standalone_test.py`
   - Result: failed with `MemoryError` during chunking (`chunk_text`) in `workflow_agents/base_agents.py`.
   - Interpretation: this validated the instability scenario that motivated the chunking hardening and controlled validation approach.

## Rubric Alignment Note
- The six non-RAG Phase 1 scripts produced successful outputs.
- The RAG script exposed a runtime stability issue (captured and documented), which drove the stabilization work completed afterward.