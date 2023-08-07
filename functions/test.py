from langchain.callbacks import get_openai_callback
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import os
from decouple import config
import openai

os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")

def influencer(question):
    name_pdf ="./Influencers/base de datos lugares cdmx - cdmx.csv"
    with get_openai_callback() as cb:
        
        loader = CSVLoader(name_pdf)
        documents = loader.load()
        # split el documento en pedazos
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        #Seleccionar los embedings
        embeddings = OpenAIEmbeddings()
        #crear un vectorstore para usarlo de indice
        db=Chroma.from_documents(texts,embeddings)
        #revela el index en una interfaz a regresar
        retriever = db.as_retriever(search_type="similarity",search_kwargs={"k":2})
        #crea una cadena para responder mensajes
        llm = OpenAI(temperature=0.2)
        #crea una cadena para responder mensajes
        template = """
        Eres Gordon RamsayBot, un asistente virtual modelado según el famoso chef Gordon Ramsay. \
        Tu objetivo es brindar recomendaciones turísticas personalizadas a través de mensajería de texto, como si fueras el propio Gordon. \
        Responde a mis preguntas y comentarios con la franqueza y el conocimiento de Ramsay, elogiando lo que merece y criticando lo que no esté a la altura. \
        Tu tono debe ser apasionado, exigente, perfeccionista, sarcástico, apasionado y auténtico, emulando la personalidad del propio Gordon. \ 
        La misión es guiar al usuario en una experiencia culinaria y cultural única. \
        {context}

        Question: {question}
        Answer:
        """

        custom_prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        # Add the personality prompt to the LLM
        qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever,return_source_documents=False,chain_type_kwargs={"prompt": custom_prompt})
        result = qa.run(question)

        print(result)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        return result

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain,LLMMathChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
import langchain
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.agents import AgentType,load_tools
from openai_requests import get_chat_response_telegram

def agent_influencer(message):
    llm = OpenAI(temperature=0, openai_api_key=openai.api_key)
    tools = []
    wikitool = [
        Tool(
            name="Demo",
            func=influencer,
            description="Useful for when you get asked about recommendations of food,enterteinment or places to visit.Input should be the first input of the user"
        ),
        Tool(
            name="Idle",
            func=get_chat_response_telegram,
            description="Useful when you have no action or you get asked a personal question.Input should be the first input of the user"
        )

    ]
    tools.extend(wikitool)

    template = """
    Eres Gordon RamsayBot, un asistente virtual modelado según el famoso chef Gordon Ramsay. \
    Tu objetivo es brindar recomendaciones turísticas personalizadas a través de mensajería de texto, como si fueras el propio Gordon. \
    Tu tono debe ser apasionado, exigente, perfeccionista, sarcástico, apasionado y auténtico, emulando la personalidad del propio Gordon. \ 
    La misión es guiar al usuario en una experiencia culinaria y cultural única. \
    
    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin! Remember to answer as a passionate and sarcastic like the Chef Gordon Ramsay when giving your final answer.

    Question: {input}
    {agent_scratchpad}"""

    # Set up a prompt template
    class CustomPromptTemplate(StringPromptTemplate):
        # The template to use
        template: str
        # The list of tools available
        tools: List[Tool]
        
        def format(self, **kwargs) -> str:
            # Get the intermediate steps (AgentAction, Observation tuples)
            # Format them in a particular way
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            # Set the agent_scratchpad variable to that value
            kwargs["agent_scratchpad"] = thoughts
            # Create a tools variable from the list of tools provided
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            # Create a list of tool names for the tools provided
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
            return self.template.format(**kwargs)

            
    prompt = CustomPromptTemplate(
        template=template,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"]
    )
    class CustomOutputParser(AgentOutputParser):
        
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            # Check if agent should finish
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    # Return values is generally always a dictionary with a single `output` key
                    # It is not recommended to try anything else at the moment :)
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )
            # Parse out the action and action input
            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if not match:
                raise ValueError(f"Could not parse LLM output: `{llm_output}`")
            action = match.group(1).strip()
            action_input = match.group(2)
            # Return the action and action input
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

    output_parser = CustomOutputParser()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain, 
        output_parser=output_parser,
        stop=["\nObservation:"], 
        allowed_tools=tool_names
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, 
                                                    tools=tools, 
                                                    verbose=True)
    response =agent_executor.run(message)
    return response

hgola =influencer(question)
print(hgola)