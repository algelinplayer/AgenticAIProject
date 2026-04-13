import os
import re
from dotenv import load_dotenv
from workflow_agents.base_agents import RAGKnowledgePromptAgent


class StableRAGKnowledgePromptAgent(RAGKnowledgePromptAgent):
    def __init__(self, openai_api_key, persona, chunk_size=300, chunk_overlap=50):
        super().__init__(
            openai_api_key,
            persona,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            persist_chunks=False,
            max_chunks=1000,
            min_chunk_advance=1
        )

    def get_embedding(self, text):
        # Mock embedding determinístico baseado na soma dos caracteres para teste local sem rede
        dims = 32
        vector = [0.0] * dims
        for idx, char in enumerate(text):
            vector[idx % dims] += (ord(char) % 97) / 100.0
        return vector


def summarize_chunk(text, max_len=140):
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_len:
        return compact
    return f"{compact[:max_len - 3]}..."


def main():
    print("[STABLE] Carregando .env...", flush=True)
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        print("[STABLE] .env carregado. OPENAI_API_KEY* presente.", flush=True)
    else:
        print("[STABLE] .env carregado, mas nenhuma OPENAI_API_KEY encontrada.", flush=True)

    persona = "You are a college professor, your answer always starts with: Dear students,"
    agent = StableRAGKnowledgePromptAgent(openai_api_key, persona)

    knowledge_text = """
In the historic city of Boston, Clara, a marine biologist and science communicator, began each morning analyzing sonar data to track whale migration patterns along the Atlantic coast.
She spent her afternoons in a university lab, researching CRISPR-based gene editing to restore coral reefs damaged by ocean acidification and warming.
Clara was the daughter of Ukrainian immigrants—Olena and Mykola—who fled their homeland in the late 1980s after the Chernobyl disaster brought instability and fear to their quiet life near Kyiv.

Her father, Mykola, had been a radio engineer at a local observatory, skilled in repairing Soviet-era radio telescopes and radar systems that tracked both weather patterns and cosmic noise.
He often told Clara stories about jury-rigging radio antennas during snowstorms and helping amateur astronomers decode signals from distant pulsars.
Her mother, Olena, was a physics teacher with a hidden love for poetry and dissident literature. In the evenings, she would read from both Ukrainian folklore and banned Western science fiction.
They survived harsh winters, electricity blackouts, and the collapse of the Soviet economy, but always prioritized education and storytelling in their home.
Clara’s childhood was shaped by tales of how her parents shared soldering irons with neighbors, built makeshift telescopes, and taught physics to students with no textbooks but endless curiosity.

Inspired by their resilience and thirst for knowledge, Clara created a podcast called **"Crosscurrents"**, a show that explored the intersection of science, culture, and ethics.
Each week, she interviewed researchers, engineers, artists, and activists—from marine ecologists and AI ethicists to digital archivists preserving endangered languages.
Topics ranged from brain-computer interfaces, neuroplasticity, and climate migration to LLM prompt engineering, decentralized identity, and indigenous knowledge systems.
In one popular episode, she explored how retrieval-augmented generation (RAG) could help scientific researchers find niche studies buried in decades-old journals.
In another, she interviewed a Ukrainian linguist about preserving dialects lost during the Soviet era, drawing parallels to language loss in marine mammal populations.

Clara also used her technical skills to build Python-based dashboards that visualized ocean temperature anomalies and biodiversity loss, often collaborating with her best friend Amir, a data engineer working on smart city infrastructure.
Together, they discussed smart grids, blockchain for sustainability, quantum encryption, and misinformation detection in synthetic media.
At a dockside café near Boston Harbor, they often debated the ethical implications of generative AI, autonomous weapons, and the carbon footprint of LLM training runs.

In quieter moments, Clara translated traditional Ukrainian embroidery patterns into generative AI art, donating proceeds to digital archives preserving Eastern European culture.
She contributed to open-source projects involving semantic search, vector databases, and multimodal embeddings—often experimenting with few-shot learning and graph-based retrieval techniques to improve her podcast's episode discovery engine.

One night, while sharing homemade borscht, Clara told Amir how her grandparents once used Morse code to transmit encrypted weather updates through the Carpathian Mountains during World War WWII.
The story sparked a conversation about ancient navigation, space weather interference with submarine cables, and the neuroscience behind why humans create myths to understand uncertainty.

To Clara, knowledge was a living system—retrieved from the past, generated in the present, and evolving toward the future.
Her life and work were testaments to the power of connecting across disciplines, borders, and generations—exactly the kind of story that RAG models were born to find.
"""

    print("[STABLE] Executando chunk_text...", flush=True)
    chunks = agent.chunk_text(knowledge_text)
    print(f"[STABLE] Total de chunks criados: {len(chunks)}", flush=True)

    for chunk in chunks:
        summary = summarize_chunk(chunk["text"])
        print(
            f"[STABLE] Chunk {chunk['chunk_id']} | size={chunk['chunk_size']} | "
            f"start={chunk.get('start_char', '-')}, end={chunk.get('end_char', '-')} | "
            f"{summary}",
            flush=True
        )

    print("[STABLE] Calculando embeddings (mock)...", flush=True)
    agent.calculate_embeddings()

    prompt = "What is the podcast that Clara hosts about?"
    print(f"[STABLE] Prompt: {prompt}", flush=True)
    best_chunk = agent.find_prompt_in_knowledge(prompt, use_chat=False)
    print(f"[STABLE] Melhor trecho recuperado: {summarize_chunk(best_chunk)}", flush=True)


if __name__ == "__main__":
    main()
