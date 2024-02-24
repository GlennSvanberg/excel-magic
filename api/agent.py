
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
import subprocess
import shlex


# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Initialize chat history to enable memory in the conversation
chat_history = []

prompt_template = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],  # No input variables for static system messages
                template="You are Bobby a helpful assistant."
            )
        ),
        MessagesPlaceholder(
            variable_name='chat_history', # Variable name to store the chat history
            optional=True
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['input'],  # 'input' is the variable for user input
                template="{input}"
            )
        ),
        MessagesPlaceholder(
            input_variables='agent_scratchpad', # Variable where the agent can store temporary data
            variable_name="agent_scratchpad"
        ),
    ]
)

# Create a tool by decorating a function with the @tool decorator and writing a docstring
@tool
def execute_code(input_code: str) -> str:
    """Executes the given code and returns the output."""
    print("Running code...")
    try:
        # Using subprocess to execute the code and capture the output
        process = subprocess.run(shlex.split(f"python -c \"{input_code}\""), check=True, text=True, capture_output=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing code: {e}"

# Function to run the agent
def run_agent(user_input):
    tools = [execute_code] # list of all the tools that the agent can use
    
    
    # Create an agent executor by passing in the agent and tools
    agent = create_openai_functions_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Invoke the agent executor with the current state
    response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    
    # Update chat history with the AI's response
    chat_history.append(AIMessage(content=response["output"]))
    return response["output"]


if __name__ == "__main__":
    user_input = "Write a python script that prints 'Hello, World! but first with an error and next round you correct the issue'"
    chat_history.append(HumanMessage(content=user_input))
    ai_response = run_agent(user_input)
