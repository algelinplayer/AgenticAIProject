from workflow_agents.base_agents import RAGKnowledgePromptAgent
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY_DEV') or os.getenv('OPENAI_API_KEY')
persona = 'Dear students, I am your professor.'
agent = RAGKnowledgePromptAgent(openai_api_key, persona, 500, 50)
knowledge_text = 'The Eiffel Tower is in Paris, France.'
agent.chunk_text(knowledge_text)
agent.calculate_embeddings()
print(agent.find_prompt_in_knowledge('Where is the Eiffel Tower?'))
