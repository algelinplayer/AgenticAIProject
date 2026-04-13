import os
import sys
from dotenv import load_dotenv
from workflow_agents.base_agents import RAGKnowledgePromptAgent

def main():
    print("[REAL-V2] Carregando .env...", flush=True)
    load_dotenv()
    
    # Priorizar OPENAI_API_KEY_DEV conforme padrão do curso
    api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("[REAL-V2] ERRO: OPENAI_API_KEY não encontrada no .env", flush=True)
        return

    print("[REAL-V2] Inicializando RAGKnowledgePromptAgent com API Real...", flush=True)
    persona = "You are a helpful assistant."
    agent = RAGKnowledgePromptAgent(
        openai_api_key=api_key, 
        persona=persona, 
        chunk_size=500, 
        chunk_overlap=50,
        persist_chunks=False # Desativar CSV para evitar travamento de I/O
    )

    knowledge_text = """
    The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. 
    It is named after the engineer Gustave Eiffel, whose company designed and built the tower. 
    Constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France.
    """

    print("[REAL-V2] Executando chunk_text...", flush=True)
    agent.chunk_text(knowledge_text)
    print(f"[REAL-V2] Total de chunks: {len(agent.chunks)}", flush=True)

    print("[REAL-V2] Calculando Embeddings REAIS (OpenAI)...", flush=True)
    try:
        agent.calculate_embeddings()
        print("[REAL-V2] Embeddings calculados com sucesso.", flush=True)
    except Exception as e:
        print(f"[REAL-V2] ERRO ao calcular embeddings: {e}", flush=True)
        return

    prompt = "Who designed the Eiffel Tower?"
    print(f"[REAL-V2] Buscando resposta para: '{prompt}'", flush=True)
    
    try:
        response = agent.find_prompt_in_knowledge(prompt)
        print("\n[REAL-V2] RESPOSTA FINAL DO AGENTE:", flush=True)
        print("-" * 30, flush=True)
        print(response, flush=True)
        print("-" * 30, flush=True)
    except Exception as e:
        print(f"[REAL-V2] ERRO ao buscar resposta: {e}", flush=True)

if __name__ == "__main__":
    main()
