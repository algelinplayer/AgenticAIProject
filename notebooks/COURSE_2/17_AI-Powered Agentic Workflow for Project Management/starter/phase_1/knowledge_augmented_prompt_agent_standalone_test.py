from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
from pathlib import Path
env_path = Path(__file__).resolve().parents[1] / "tests" / ".env"
load_dotenv(env_path)

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
response = knowledge_agent.respond(prompt)

print(response)
print("This response should reflect the provided knowledge (London), not the model's general knowledge.")
