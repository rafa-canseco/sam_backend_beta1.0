from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
import langchain
import openai
from langchain.agents import tools
from langchain.agents import load_tools
from langchain.agents import initialize_agent,Tool
#para wikipedia
from langchain.agents import AgentType,load_tools
from langchain.utilities import WikipediaAPIWrapper
# from langchain.tools import  DuckDuckGoSearchRun ,BaseTool
from langchain.callbacks import get_openai_callback
import ssl
from langchain import OpenAI
from decouple import config
import os
import openai
from openai_requests import get_chat_response_telegram,get_treatment
from langchain.chains.conversation.memory import ConversationBufferMemory


os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")
ZAPIER_NLA_API_KEY=config("ZAPIER_NLA_API_KEY")
SERPAPI_API_KEY =config("SERPAPI_API_KEY")
WOLFRAM_ALPHA_APPID= config("WOLFRAM_ALPHA_APPID")
wikipedia = WikipediaAPIWrapper()


llm = OpenAI(temperature=0, openai_api_key=openai.api_key)
tool_names = ["serpapi","wikipedia","llm-math"]
tools = load_tools(tool_names,serpapi_api_key=SERPAPI_API_KEY,wikipedia= wikipedia,llm=llm)

tool_names = ["serpapi", "wikipedia", "llm-math"]
tools = load_tools(tool_names, serpapi_api_key=SERPAPI_API_KEY, wikipedia=wikipedia, llm=llm)

# Iterar sobre cada herramienta y mostrar su información
for tool in tools:
    print(f"Name: {tool.name}")
    print(f"Function: {tool.func}")
    print(f"Description: {tool.description}")
    print("------------------------")
