from dotenv import load_dotenv
import pandas as pd
import os
import openai
import json
import numpy as np
from langchain.llms import AzureOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.prompts.chat import ChatPromptTemplate
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")
OPENAI_API_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")
openai.api_type = "azure"
openai.api_base = OPENAI_DEPLOYMENT_ENDPOINT
openai.api_key = OPENAI_API_KEY
MODEL_NAME = "gpt-35-turbo"
openai.api_version = "2022-12-01"
AAD_TENANT_ID = os.getenv("AAD_TENANT_ID")
# Initiate a connection to the LLM from Azure OpenAI Service via LangChain.
def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """
    agent = create_csv_agent(AzureOpenAI(openai_api_key=OPENAI_API_KEY, 
                           deployment_name=OPENAI_DEPLOYMENT_NAME, 
                           model_name=MODEL_NAME), filename)
    return agent

def query_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """
    prompt = (
        """

        Below is the query.
            Query:
            """
        + query
    )
    response = agent.run(prompt)
    print(response)
    return response.__str__()
