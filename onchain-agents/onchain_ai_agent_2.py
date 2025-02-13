from dotenv import load_dotenv
import os
from openai import OpenAI
from transformers import pipeline
import google.generativeai as genai
from llm_tools import process_with_openai, process_with_flan_t5, process_with_gemini
from tool_registry import determine_action
from system_prompt import DEFAULT_SYSTEM_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from blockchain_utils import get_balance, get_transaction  # new import

# Load environment variables
load_dotenv()

# Configure OpenAI client using key from .env (if needed here)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure Hugging Face FLAN-T5
flan_t5_model = pipeline("text2text-generation", model="google/flan-t5-small")

# Configure Google Gemini (via google.generativeai) using key from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = "gemini-1.5-flash"

# New: Define tools using LangGraph-compatible format
tools = [
    Tool(
        name="get_balance",
        func=get_balance,
        description="Checks the balance of a given wallet address.",
    ),
    Tool(
        name="get_transaction",
        func=get_transaction,
        description="Retrieves transaction details given a transaction hash.",
    ),
]

# Replace the prompt_template with a partial prompt to default "agent_scratchpad"
prompt_template = PromptTemplate(
    input_variables=["input", "tools", "agent_scratchpad", "tool_names"],
    template="""You are a helpful blockchain assistant that can use the following tools:
Tools: {tools}
Tool names: {tool_names}

Work through the problem step by step. Use the scratchpad to reason.
After calling one or more tools, analyze their outputs and provide a friendly summary that highlights the key information.
Now, answer the user's query:
{input}""",
).partial(agent_scratchpad="")


# Group LLM configuration functions for clarity:
def configure_openai(system_prompt):
    def llm_func(prompt):
        return process_with_openai(prompt, system_prompt)

    return llm_func


def configure_flan_t5(system_prompt):
    def llm_func(prompt):
        return process_with_flan_t5(prompt, system_prompt)

    return llm_func


def configure_gemini(system_prompt):
    def llm_func(prompt):
        return process_with_gemini(prompt, system_prompt)

    return llm_func


def configure_langgraph():
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4")
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def llm_func(prompt):
        inputs = {
            "input": prompt,
            "agent_scratchpad": "",
            "tool_names": ", ".join([tool.name for tool in tools]),
            "tools": ", ".join([f"{tool.name}: {tool.description}" for tool in tools]),
        }
        return agent_executor.run(inputs)

    return llm_func


# 7. Chatbot logic
def onchain_ai_agent_2():
    print("AI Chatbot is ready! Ask me anything or perform Berachain actions.")
    print("Type 'exit' or 'quit' to end the chat.")

    # Read the system prompt or fallback to default
    user_input = input(
        "Set the system prompt for the chatbot (leave empty to use default): "
    ).strip()
    system_prompt = user_input if user_input else DEFAULT_SYSTEM_PROMPT

    # Choose a language model
    print("Choose your LLM model:")
    print("1: OpenAI GPT")
    print("2: Hugging Face FLAN-T5 (Google FLAN)")
    print("3: Google Gemini (gemini-1.5-flash)")
    print("4: LangGraph Agent (ReAct with custom tools)")
    model_choice = input("Enter your choice: ").strip()

    # Configure llm_function based on choice
    if model_choice == "1":
        llm_function = configure_openai(system_prompt)
        print("Using OpenAI GPT.")
    elif model_choice == "2":
        llm_function = configure_flan_t5(system_prompt)
        print("Using Hugging Face FLAN-T5.")
    elif model_choice == "3":
        llm_function = configure_gemini(system_prompt)
        print("Using Google Gemini.")
    elif model_choice == "4":
        llm_function = configure_langgraph()
        print("Using LangGraph ReAct Agent.")
    else:
        print("Invalid choice. Restart and choose 1, 2, 3, or 4.")
        return

    # Main chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # First try to process any direct tool actions
        action_response = determine_action(user_input)
        if action_response is not None:
            print(f"Agent: {action_response}")
        else:
            response = llm_function(user_input)
            print(f"Agent: {response}")


if __name__ == "__main__":
    onchain_ai_agent_2()
