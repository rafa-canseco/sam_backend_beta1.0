from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.agents import AgentType,load_tools,Tool
from langchain.utilities import WikipediaAPIWrapper 
import os
import openai
from decouple import config
from langchain.callbacks import get_openai_callback
import ssl
from langchain.tools import  DuckDuckGoSearchTool ,BaseTool



os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")
ZAPIER_NLA_API_KEY=config("ZAPIER_NLA_API_KEY")
SERPAPI_API_KEY =config("SERPAPI_API_KEY")
WOLFRAM_ALPHA_APPID= config("WOLFRAM_ALPHA_APPID")
wikipedia = WikipediaAPIWrapper()


with get_openai_callback() as cb:
        
        message_decoded = """busca con duck duck go el precio de ripple"""
        ssl._create_default_https_context = ssl._create_stdlib_context
        llm = OpenAI(temperature=0,openai_api_key=openai.api_key)
        tool_names = ["serpapi","wolfram-alpha","wikipedia","llm-math"]
        tools = load_tools(tool_names,serpapi_api_key=SERPAPI_API_KEY,wolfram_alpha_appid=WOLFRAM_ALPHA_APPID,wikipedia= wikipedia,llm=llm)
        search_duck = DuckDuckGoSearchTool()
        duckduckgotool_duck = [Tool(
                name='DuckDuckGo Search',
                func =search_duck.run,
                description="useful for when you need to do a search on the internet to find information that another tool cant find.Be specific with your input"
        )]
        tools.extend(duckduckgotool_duck)
        agent = initialize_agent(tools, llm ,agent="zero-shot-react-description",verbose=True)
        response = agent.run(message_decoded)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")