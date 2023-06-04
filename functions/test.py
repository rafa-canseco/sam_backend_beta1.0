from kor import create_extraction_chain, Object, Text, Number
import json
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
import openai
from decouple import config


os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")

user="rafa.canseco@gmail.com"
cred = credentials.Certificate("samai-b9f36-firebase-adminsdk-4lk6x-ee898f95b0.json")
firebase_admin.initialize_app(cred)
firebase_app =firebase_admin.get_app()

def abstraction(user):
    with get_openai_callback() as cb:
        
        with get_openai_callback() as cb:
            storage_client = storage.bucket("samai-b9f36.appspot.com")
            folder_name = f"{user}/{user}_workflow"
            file_name = f"{folder_name}/test_data_{user}.txt"

            # Crear el directorio de destino si no existe
            os.makedirs(folder_name, exist_ok=True)

            blob = storage_client.blob(file_name)
            archivo_destino = f"./{file_name}"
            blob.download_to_filename(archivo_destino)

            with open(archivo_destino, "r") as f:
                contenido = f.read()
                print(contenido)
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            max_tokens=2000,
            openai_api_key=openai.api_key
        )
        person_schema = Object(
            id="person",
            description="Personal information about a person",
            
            # Notice I put multiple fields to pull out different attributes
            attributes=[
                Text(
                    id="first_name",
                    description="Primer nombre de una persona"
                ),
                Text(
                    id="apellido",
                    description="apellido de la persona"
                ),
                Text(
                    id="number",
                    description="número telefónico de la persona"
                ),
                 Text(
                    id="mail",
                    description="correo electrónico de la persona"
                ),
                Text(
                    id="edad",
                    description="edad de la persona"
                ),
                 Text(
                    id="residencia",
                    description="lugar de residencia"
                ),
            ],
            examples=[
                (
                    "mi nombre es rafa canseco, mi numero es 2211802557, mi correo es rafa.canseco@gmail.com, tengo 30 años, soy de la ciudad de puebla",
                    [
                        {"first_name": "rafa"},
                        {"apellido": "canseco"},
                        {"number": "2211802557"},
                        {"mail": "rafa.canseco@gmail.com"},
                        {"edad": "30"},
                        {"residencia": "puebla"},
                    ],
                )
            ]
        )



        chain = create_extraction_chain(llm, person_schema)
        response = chain.predict_and_parse(text=contenido)
        print(response)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        return response


hola = abstraction(user)