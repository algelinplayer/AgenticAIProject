import os
import re
from dotenv import load_dotenv


class SafeRAGChunkingAgent:
    def __init__(self, openai_api_key, persona, chunk_size=300, chunk_overlap=50):
        print(f"[SAFE] Criando agente. Persona: {persona[:30]}...", flush=True)
        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = openai_api_key

    def chunk_text(self, text):
        print(f"[SAFE] Iniciando chunk_text. Tamanho total: {len(text)}", flush=True)
        separator = "\n"
        text = re.sub(r"[ \t]+", " ", text).strip()

        if len(text) <= self.chunk_size:
            print(f"[SAFE] Texto menor que chunk_size ({self.chunk_size}). Único chunk criado.", flush=True)
            return [{"chunk_id": 0, "text": text, "chunk_size": len(text)}]

        chunks, start, chunk_id = [], 0, 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if separator in text[start:end]:
                end = start + text[start:end].rindex(separator) + len(separator)

            chunk_content = text[start:end]
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_content,
                "chunk_size": len(chunk_content),
                "start_char": start,
                "end_char": end
            })

            if end == len(text):
                break

            new_start = end - self.chunk_overlap
            if new_start <= start:
                print(f"[SAFE] Ajuste de segurança: new_start {new_start} <= start {start}. Avançando.", flush=True)
                start = end
            else:
                start = new_start

            chunk_id += 1
            if chunk_id > 1000:
                print("[SAFE] Muitos chunks gerados (>1000). Abortando para evitar loop.", flush=True)
                break

        return chunks


def summarize_chunk(text, max_len=120):
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_len:
        return compact
    return f"{compact[:max_len - 3]}..."


def main():
    print("[SAFE] Carregando .env...", flush=True)
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        print("[SAFE] .env carregado. OPENAI_API_KEY* presente.", flush=True)
    else:
        print("[SAFE] .env carregado, mas nenhuma OPENAI_API_KEY encontrada.", flush=True)

    persona = "You are a college professor, your answer always starts with: Dear students,"
    agent = SafeRAGChunkingAgent(openai_api_key, persona, chunk_size=300, chunk_overlap=50)

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

One night, while sharing homemade borscht, Clara told Amir how her grandparents once used Morse code to transmit encrypted weather updates through the Carpathian Mountains during World War II.
The story sparked a conversation about ancient navigation, space weather interference with submarine cables, and the neuroscience behind why humans create myths to understand uncertainty.

To Clara, knowledge was a living system—retrieved from the past, generated in the present, and evolving toward the future.
Her life and work were testaments to the power of connecting across disciplines, borders, and generations—exactly the kind of story that RAG models were born to find.
"""
    print("[SAFE] Executando chunk_text...", flush=True)
    chunks = agent.chunk_text(knowledge_text)
    print(f"[SAFE] Total de chunks criados: {len(chunks)}", flush=True)

    for chunk in chunks:
        summary = summarize_chunk(chunk["text"])
        print(
            f"[SAFE] Chunk {chunk['chunk_id']} | size={chunk['chunk_size']} | "
            f"start={chunk.get('start_char', '-')}, end={chunk.get('end_char', '-')} | "
            f"{summary}",
            flush=True
        )


if __name__ == "__main__":
    main()
