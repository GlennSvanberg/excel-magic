
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
import subprocess
import shlex
import os
import pandas as pd
import shutil
# Initialize the language model
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

prompt_template = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],  # No input variables for static system messages
                template="""You are a helpful Excel expert assistant that help create, 
                modify merge and analyze Excel files using pandas and openpyxl. 
                You are always helpful and friendly but short and to the point. 
                You do not modify the files directly, but instead create a new file with the modifications.
                """
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


@tool
def execute_code(input_code: str) -> str:
    """Executes the given python code in the playground and returns the output from the terminal. 
    Use this function to modify excel files and create new excel files. 
    The name of the new excelfile should be descriptive of what the file contains and have a random number as a suffix to avoid overwriting existing files."""
    print("Running code in /playground...")
    try:
        # print current dir
        print(os.getcwd())
        # Change the current working directory to /playground
        os.chdir('playground')
        # Using subprocess to execute the code and capture the output
        process = subprocess.run(shlex.split(f"python -c \"{input_code}\""), check=True, text=True, capture_output=True)
        # Change back to the original directory after execution
        os.chdir('..')
        return process.stdout
    
    except subprocess.CalledProcessError as e:
        # Change back to the original directory in case of an exception
        os.chdir('..')
        return f"Error executing code: {e}"

def copy_file_to_playground(filename):
    """Copy the file from /uploads to /playground without moving it, ensuring the original file remains in /uploads."""
    try:
        # Copy the file from /uploads to /playground without removing it from /uploads
        shutil.copy(f'uploads/{filename}', f'playground/{filename}')
        return f"File {filename} copied to /playground"
    except Exception as e:
        return f"Error copying file: {e}"

def copy_file_to_uploads_and_output(filename):
    """Copy the file from /playground to both /uploads and /static/output"""
    messages = []
    try:
        # Copy the file from /playground to /uploads
        shutil.copy(f'playground/{filename}', f'uploads/{filename}')
        messages.append(f"File {filename} copied to /uploads")
    except Exception as e:
        messages.append(f"Error copying file to /uploads: {e}")
    try:
        # Copy the file from /playground to /static/output
        shutil.copy(f'playground/{filename}', f'static/output/{filename}')
        messages.append(f"File {filename} copied to /static/output")
    except Exception as e:
        messages.append(f"Error copying file to /static/output: {e}")
    return "\n".join(messages)

def clear_playground():
    """Clear the /playground folder"""
    try:
        # Remove all files from /playground
        for file in os.listdir('playground'):
            os.remove(f'playground/{file}')
        return "Playground cleared"
    except Exception as e:
        return f"Error clearing playground: {e}"
    
def find_files_in_playground_that_are_not_in_input():
    """Find files in /playground that are not in /uploads"""
    try:
        # Get the list of files in /uploads and /playground
        files_in_uploads = os.listdir('uploads')
        files_in_playground = os.listdir('playground')
        # Find the files in /playground that are not in /uploads
        files_not_in_input = list(set(files_in_playground) - set(files_in_uploads))
        print(f"Files in /playground that are not in /uploads: {files_not_in_input}")
        return files_not_in_input
    except Exception as e:
        return f"Error finding files: {e}"
    

# Function to run the agent
def run_agent(user_input, chat_history=[]):
    tools = [execute_code] # list of all the tools that the agent can use
    
    # Create an agent executor by passing in the agent and tools
    agent = create_openai_functions_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Invoke the agent executor with the current state
    response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    
    # Update chat history with the AI's response
    chat_history.append(AIMessage(content=response["output"]))
    return response["output"]

# print head and filename for each excel file in playground
def print_files_in_playground():
    files = os.listdir('playground')
    for file in files:
        if file.endswith('.xlsx'):
            df = pd.read_excel(f'playground/{file}')
            print(f"File: {file}")
            print(df.head())
            print("\n")

def work_on_files(files):
    for file in files:
        copy_file_to_playground(file)

    return "Files copied to /playground"

def get_file_data(files):
    file_data = []
    for file in files:
        df = pd.read_excel(f'playground/{file}')
        print(f"Processing file: {file}")
        print("df.head():")
        print(df.head())  # This line mimics the exact output as df.head() printed to the console
        # Capturing the output of df.head() as it would appear in the console
        head_as_string = df.head().to_string()
        res = {
            "filename": file,
            "head": head_as_string
        }
        file_data.append(res)
    file_data = str(file_data)
    return file_data

def add_message_to_chat_history(messages, chat_history):
    for message in messages[:-1]:  # Exclude the last message from processing
        if message["sender"] == "AI":
            chat_history.append(AIMessage(content=message["message"]))
        else:
            chat_history.append(HumanMessage(content=message["message"]))
    return chat_history

def do_magic(files, messages):
    chat_history = add_message_to_chat_history(messages, [])
    work_on_files(files)
    file_data = get_file_data(files)
    # Assuming the last message in the messages list is the user's input
    user_input = messages[-1]["message"] if messages and messages[-1]["sender"] == "User" else "No user input found."
    user_input = f"You have access to the files: {file_data}\n{user_input}"
    print(user_input)

    chat_history.append(HumanMessage(content=user_input))
    ai_response = run_agent(user_input, chat_history)
    print_files_in_playground()
    
    files = find_files_in_playground_that_are_not_in_input()
    for file in files:
        copy_file_to_uploads_and_output(file)
    clear_playground()

    return files, ai_response
def get_head_of_file(file):
    df = pd.read_excel(f'uploads/{file}')
    return df.head()

if __name__ == "__main__":
    chat_history = []
    files = ["data.xlsx", "names.xlsx"]
    work_on_files(files)
    file_data = get_file_data(files)
    user_input = f"Join the files on the column name and keep all rows from both files"
    messages = []
    ai_message= "Hi how may I help you today?"

    messages.append({"sender":"AI", "message": ai_message})
    messages.append({"sender":"User", "message": user_input})


    do_magic(files, messages)