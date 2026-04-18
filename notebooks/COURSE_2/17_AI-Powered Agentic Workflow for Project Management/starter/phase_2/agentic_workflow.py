# agentic_workflow.py

import importlib
import os
import sys
from pathlib import Path

# Add starter directory to sys.path and load phase_1 workflow agents
phase_2_dir = Path(__file__).resolve().parent
phase_1_dir = phase_2_dir.parent / "phase_1"
starter_dir = phase_1_dir.parent
if str(starter_dir) not in sys.path:
    sys.path.append(str(starter_dir))

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
base_agents_module = importlib.import_module("phase_1.workflow_agents.base_agents")
ActionPlanningAgent = base_agents_module.ActionPlanningAgent
KnowledgeAugmentedPromptAgent = base_agents_module.KnowledgeAugmentedPromptAgent
EvaluationAgent = base_agents_module.EvaluationAgent
RoutingAgent = base_agents_module.RoutingAgent
from dotenv import load_dotenv

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
env_path = phase_2_dir.parent / "tests" / ".env"
load_dotenv(env_path)
openai_api_key = os.getenv("OPENAI_API_KEY_DEV") or os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY_DEV or OPENAI_API_KEY not found in .env file.")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
product_spec_path = phase_2_dir / "Product-Spec-Email-Router.txt"
with open(product_spec_path, "r", encoding="utf-8") as file:
    product_spec = file.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = (
    "You are a Product Manager. Your ONLY goal is to generate user stories for the Email Router. "
    "You MUST NOT include any introductory text, grouping headers, or conversational meta-talk. "
    "Each story must be a single line following a strict template."
)
knowledge_product_manager = (
    "Every user story MUST follow this exact format: 'As a [type of user], I want [an action or feature] so that [benefit/value].' "
    "persona: user of the system (e.g., Customer, Support Agent, SME, IT Admin). "
    "action: specific functionality. "
    "outcome: the value provided. "
    "Strictly avoid 'I need' or other variations. "
    "Do NOT include planning prose or grouping summaries."
    f"\n\nProduct Specification:\n{product_spec}"
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_pm_eval = "You are a strict Auditor that ensures User Stories follow a precise syntax."
criteria_pm_eval = (
    "1. Every single line MUST match: 'As a [type of user], I want [an action or feature] so that [benefit/value].'\n"
    "2. NO introductory text (e.g., 'Here are the stories...').\n"
    "3. NO grouping headers or planning commentary.\n"
    "4. 'I want' is mandatory; 'I need' is FORBIDDEN."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_pm_eval,
    evaluation_criteria=criteria_pm_eval,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=3,
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = (
    "You are a Program Manager. Your ONLY goal is to define product features based on the Email Router specification. "
    "You MUST NOT include grouping essay text, planning prose, or off-topic features (like payments)."
)
knowledge_program_manager = (
    "Each feature MUST follow this exact 4-label structure:\n"
    "Feature Name: [Title]\n"
    "Description: [Brief explanation]\n"
    "Key Functionality: [Specific capabilities]\n"
    "User Benefit: [Value]\n\n"
    "Focus ONLY on Email Router features: automated ingestion, NLP classification, RAG-based SME routing, analytics dashboard, etc. "
    "Reject anything unrelated to Email Routing. Do NOT include 'Grouping similar stories' or other prose."
)
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are a strict Auditor that ensures Product Features follow the required structure and scope."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
criteria_program_manager_eval = (
    "1. Every feature MUST use exactly these four labels: 'Feature Name:', 'Description:', 'Key Functionality:', 'User Benefit:'.\n"
    "2. Features MUST be relevant to the Email Router (No payment processing or unrelated generic features).\n"
    "3. NO grouping essay text, commentary, or conversational artifacts."
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=criteria_program_manager_eval,
    worker_agent=program_manager_knowledge_agent,
    max_interactions=3,
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = (
    "You are a Development Engineer. Your ONLY goal is to define technical tasks in a strict, stable layout. "
    "You MUST NOT include meta-talk, multiple competing formats, or extra numbering."
)
knowledge_dev_engineer = (
    "Each task MUST follow this exact 7-label structure on separate lines:\n"
    "Task ID: [Unique ID]\n"
    "Task Title: [Brief description]\n"
    "Related User Story: [Parent story reference]\n"
    "Description: [Technical details]\n"
    "Acceptance Criteria: [Completion requirements]\n"
    "Estimated Effort: [Estimation]\n"
    "Dependencies: [Prerequisites]\n\n"
    "Do NOT use 'Task Identification:' or other variations. Use 'Task ID:'. "
    "Maintain a stable, repeatable layout for every task."
)
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are a strict Auditor that ensures Engineering Tasks follow the exact mandated structure."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
criteria_dev_engineer_eval = (
    "1. Every task MUST follow the exact seven-label layout: 'Task ID:', 'Task Title:', 'Related User Story:', 'Description:', 'Acceptance Criteria:', 'Estimated Effort:', 'Dependencies:'.\n"
    "2. Labels must be on their own lines.\n"
    "3. NO alternate numbering schemes or 'Task Identification' labels.\n"
    "4. NO conversational text or meta-talk."
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=criteria_dev_engineer_eval,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=3,
)


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    print(f"Executing Product Manager support function for query: {query}")
    response = product_manager_knowledge_agent.respond(query)
    evaluation = product_manager_evaluation_agent.evaluate(response)
    return evaluation['final_response']

def program_manager_support_function(query):
    print(f"Executing Program Manager support function for query: {query}")
    response = program_manager_knowledge_agent.respond(query)
    evaluation = program_manager_evaluation_agent.evaluate(response)
    return evaluation['final_response']

def development_engineer_support_function(query):
    print(f"Executing Development Engineer support function for query: {query}")
    response = development_engineer_knowledge_agent.respond(query)
    evaluation = development_engineer_evaluation_agent.evaluate(response)
    return evaluation['final_response']

routes = [
    {
        "name": "Product Manager",
        "description": "Expert in defining 'As a... I want... so that...' user stories. Use this agent ONLY for generating stories from a product spec. Does NOT handle features or engineering tasks.",
        "func": lambda x: product_manager_support_function(x)
    },
    {
        "name": "Program Manager",
        "description": "Expert in defining product features with exact labels (Feature Name, Description, Key Functionality, User Benefit). Use this agent ONLY for features. Does NOT handle user stories or tasks.",
        "func": lambda x: program_manager_support_function(x)
    },
    {
        "name": "Development Engineer",
        "description": "Expert in defining technical engineering tasks with 7 strict labels (Task ID, Task Title, Related User Story, etc.). Use this agent ONLY for tasks. Does NOT handle stories or features.",
        "func": lambda x: development_engineer_support_function(x)
    }
]

routing_agent = RoutingAgent(openai_api_key, routes)
routing_agent.agents = routes


def run_workflow(workflow_prompt="Create a complete project plan for the Email Router, including: 1) User Stories, 2) Product Features, and 3) Engineering Tasks."):
    print("\n*** Workflow execution started ***\n")
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

    print("\nDefining workflow steps from the workflow prompt")
    # TODO: 12 - Implement the workflow.
    #   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
    #   2. Initialize an empty list to store 'completed_steps'.
    #   3. Loop through the extracted workflow steps:
    #      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
    #      b. Append the result to 'completed_steps'.
    #      c. Print information about the step being executed and its result.
    #   4. After the loop, print the final output of the workflow (the last completed step).
    workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    completed_steps = []

    for i, step in enumerate(workflow_steps):
        print(f"\n--- Processing Step {i + 1}: {step} ---")
        result = routing_agent.route(step)
        completed_steps.append(result)
        print(f"Result for Step {i + 1}:\n{result}")

    print("\n*** Final Workflow Output ***")
    if completed_steps:
        # Consolidate all deliverables into one final project plan
        user_stories = []
        product_features = []
        engineering_tasks = []
        other_results = []
        
        for result in completed_steps:
            if "As a" in result:
                user_stories.append(result)
            elif "Feature Name:" in result:
                product_features.append(result)
            elif "Task ID:" in result:
                engineering_tasks.append(result)
            else:
                other_results.append(result)

        consolidated_output = "\n" + "="*50 + "\n"
        consolidated_output += "FINAL PROJECT PLAN: EMAIL ROUTER\n"
        consolidated_output += "="*50 + "\n\n"
        
        if user_stories:
            consolidated_output += "### 1. USER STORIES\n"
            consolidated_output += "\n".join(user_stories) + "\n\n"
            
        if product_features:
            consolidated_output += "### 2. PRODUCT FEATURES\n"
            consolidated_output += "\n".join(product_features) + "\n\n"
            
        if engineering_tasks:
            consolidated_output += "### 3. ENGINEERING TASKS\n"
            consolidated_output += "\n".join(engineering_tasks) + "\n\n"
            
        if other_results:
            consolidated_output += "### 4. OTHER DETAILS\n"
            consolidated_output += "\n".join(other_results) + "\n\n"

        print(consolidated_output)
        
        # Save to file for evidence
        output_file = Path("C:/Users/Colaborador/PycharmProjects/AgenticAIProject/notebooks/COURSE_2/17_AI-Powered Agentic Workflow for Project Management/starter/tests/EVIDENCES/final_output_of_the_workflow.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(consolidated_output)
        print(f"Final output saved to: {output_file}")
    else:
        print("No steps completed.")


if __name__ == "__main__":
    run_workflow()