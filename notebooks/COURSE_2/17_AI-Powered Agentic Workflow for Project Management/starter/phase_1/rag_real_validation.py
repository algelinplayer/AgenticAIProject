import os
import sys
from dotenv import load_dotenv
from workflow_agents.base_agents import RAGKnowledgePromptAgent

def main():
    print("[VALIDATION] Carregando .env...", flush=True)
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("[ERROR] OPENAI_API_KEY não encontrada no .env", flush=True)
        return

    persona = "You are a helpful science communicator."
    # Usamos persist_chunks=False para evitar I/O desnecessário nesta fase de validação
    agent = RAGKnowledgePromptAgent(
        openai_api_key, 
        persona, 
        chunk_size=500, 
        chunk_overlap=50,
        persist_chunks=False
    )

    # Texto curto para validação rápida e segura
    knowledge_text = """
    Retrieval-Augmented Generation (RAG) is a technique that combines the powers of a pre-trained LLM 
    with an external search mechanism. It retrieves relevant documents from a database and uses them 
    to provide context to the model. This reduces hallucinations and ensures the model has access 
    to the most up-to-date information.
    
    Embeddings are numerical representations of text that capture semantic meaning. 
    They are essential for finding similar documents in a RAG system.
    """

    print("[VALIDATION] Iniciando chunk_text...", flush=True)
    agent.chunk_text(knowledge_text)
    print(f"[VALIDATION] Chunks criados: {len(agent.chunks)}", flush=True)

    print("[VALIDATION] Calculando embeddings REAIS (OpenAI API)...", flush=True)
    try:
        agent.calculate_embeddings()
        print("[VALIDATION] Embeddings calculados com sucesso.", flush=True)
    except Exception as e:
        print(f"[ERROR] Falha ao calcular embeddings: {e}", flush=True)
        return

    prompt = "What are the benefits of RAG?"
    print(f"[VALIDATION] Prompt: {prompt}", flush=True)
    
    print("[VALIDATION] Buscando similaridade e gerando resposta via Chat...", flush=True)
    try:
        response = agent.find_prompt_in_knowledge(prompt)
        print(f"\n[RESPONSE]:\n{response}\n", flush=True)
    except Exception as e:
        print(f"[ERROR] Falha ao gerar resposta: {e}", flush=True)

if __name__ == "__main__":
    main()
