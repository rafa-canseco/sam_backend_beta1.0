# uvicorn main:app
# uvicorn main:app --reload



# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException,WebSocket,Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from typing import Dict
import json
import uvicorn
from telegram import Bot,Update
from telegram.ext import Updater,CallbackContext,MessageHandler,filters
import requests
from json import loads
from pydub import AudioSegment
import time
import requests
import shutil
import os



# Custom function imports
from functions.text_to_speech import convert_text_to_speech, convert_text_to_speech_single,convert_text_to_speech_telegram
from functions.openai_requests import convert_audio_to_text, get_chat_response, get_chat_response_simple,get_chat_response_telegram
from functions.database import store_messages, reset_messages, store_messages_simple,get_recent_messages_telegram, cargar_chat_ids,store_messages_telegram
from functions.newAdd import instruction,search, youtube_resume, pdf_pages, dirty_data,abstraction, blockchain_tx,url_resume, preguntar_url, preguntar_youtube, load_url,pregunta_url_resumen, pregunta_url_abierta
from functions.completion import get_completion_from_messages
from functions.analisis import resumen_opcion_multiple,vector_index,pregunta_data,borrar_contenido
from firebase_admin import credentials,storage, firestore
import firebase_admin 
import json


# Get Environment Vars
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

cred = credentials.Certificate("samai-b9f36-firebase-adminsdk-4lk6x-ee898f95b0.json")
firebase_admin.initialize_app(cred)
firebase_app =firebase_admin.get_app()

token= config("token")
ngrok_url = config("ngrok_url")
chat_id_orla = config("chat_id_orla")
chat_id_rafa = config("chat_id_rafa")
authorized_users = [chat_id_rafa,chat_id_orla]
respuesta = "texto"
bot = Bot(token=token)
# Obtener la ruta de FFmpeg
ffmpeg_path = shutil.which('ffmpeg')
print(ffmpeg_path)


# Initiate App
app = FastAPI()

def cargar_chat_ids():
    with open("chat_ids.json") as f:
        chat_ids_data = json.load(f)
    return chat_ids_data.get("chat_ids", {})



# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "https://sam-frontend-beta1-0.vercel.app",
    "https://sam-frontend-beta1-0-rcsc1.vercel.app",
    "https://sam-frontend-beta1-0-git-main-rcsc1.vercel.app"
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Crear una referencia a la colección "usuarios"
db = firestore.client()
usuarios_ref = db.collection("Telegram")
# Función para incrementar el contador de clics
def incrementar_contador_clicks(chat_id):
    try:
        # Obtener referencia al documento del usuario
        usuario_doc_ref = usuarios_ref.document(str(chat_id))
        
        # Obtener el snapshot del documento actual
        usuario_doc_snapshot = usuario_doc_ref.get()
        
        if usuario_doc_snapshot.exists:
            # El usuario ya existe en la base de datos, actualizar el contador
            contador_clicks_actual = usuario_doc_snapshot.get("contadorClicks")
            nuevo_contador_clicks = (contador_clicks_actual or 0) + 1
            
            # Actualizar el documento con el nuevo contador de clics
            usuario_doc_ref.update({"contadorClicks": nuevo_contador_clicks})
        else:
            # El usuario no existe en la base de datos, crear un nuevo documento
            usuario_doc_ref.set({"contadorClicks": 1})
            
        print("Contador de clics actualizado exitosamente")
    except Exception as e:
        print("Error al incrementar el contador de clics:", e)
        # Manejar el error según sea necesario





# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}


# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}


# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)

    # Store messages
    store_messages(message_decoded, chat_response)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")
    print(chat_response)
    
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-audio-instruction")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    instruction(message_decoded)

    return "Done"

@app.post("/post-audio-search")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    response = search(message_decoded)

    return {"response": response}

# Reset Conversation
@app.post("/youtubeResponse")
async def YT_RESUME(data: dict):
    url = data["url"]
    response = youtube_resume(url)
    return {"response": response}

@app.post("/ask_youtube")
async def Ask_youtube(data: dict):
    url = data["url"]
    question = data["question"]
    response = preguntar_youtube(url,question)
    return {"response": response}

@app.post("/urlResponse")
async def URL_RESUME(data: dict):
    url = data["url"]
    response = url_resume(url)
    return {"response": response}

@app.post("/ask_url")
async def Ask_url(data: dict):
    url = data["url"]
    question = data["question"]
    response = preguntar_url(url,question)
    return {"response": response}

#Buscar en un pdf
@app.post("/PDF")
async def Ask_pdf(data: dict):
    pdf_name = data["pdf_name"]
    question = data["question"]
    response = pdf_pages(pdf_name,question)
    return {"response": response}

#Buscar en un pdf
@app.post("/Dirty")
async def data_unstructured(data: dict):
    categorias = data["set_category"]
    data = data["data"]
    response = dirty_data(categorias,data)
    return {"response": response}

#limpiar data
@app.post("/DataAbstraction")
async def data_abstraction(requestData: dict):
    obj_global = requestData["idGlobal"]
    globalDescription = requestData["globalDescription"]
    data = requestData["data"]
    ejemplo = requestData["ejemplo"]
    attributes = requestData["attributes"]
    attributeValues = requestData["attributeValues"]
    response = abstraction(globalDescription,data, attributes,attributeValues,ejemplo,obj_global)
    return {"response": response}

# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/single-chatgpt")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)
    print("erro1")

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response_simple(message_decoded)
    print("erro2")
    

    # Store messages
    store_messages_simple(message_decoded, chat_response)
    print("error3")

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")
    print(chat_response)
    # Convert chat response to audio
    audio_output = convert_text_to_speech_single(chat_response)
    print(audio_output)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

#limpiar data
@app.post("/RandomBox")
async def save_voice(requestData: dict):
    with open("data.json", "w") as f:
        json.dump(requestData, f)
    return {"done"}


#wallet tx
@app.post("/Wallet")
async def wallet_tx(requestData: dict):
    data = requestData["tx"]
    response = blockchain_tx(data)
    
    return {"response": response}

@app.websocket("/botchat")
async def chatbot(websocket: WebSocket):
    print("recibido websocket")
    await websocket.accept()
    context = []
    prompt = ""

    # Saludar al usuario y proporcionar información sobre el bot
    context.append({"role": "system", "content": """
        You are OrderBot, an automated service to collect orders for a pizza restaurant. \
        You first greet the customer, then collect the order, \
        You wait to collect the entire order, then summarize it and check for a final \
        time if the customer wants to add anything else. \
        Ask for the name of the customer. \
        Finally, you collect the payment. \
        Make sure to clarify all options, extras, and sizes to uniquely \
        identify the item from the menu.\
        You respond in a short, very conversational friendly style. \ \
        The menu includes: \
        pepperoni pizza  12.95, 10.00, 7.00 \
        cheese pizza   10.95, 9.25, 6.50 \
        eggplant pizza   11.95, 9.75, 6.75 \
        fries 4.50, 3.50 \
        greek salad 7.25 \
        Toppings: \
        extra cheese 2.00, \
        mushrooms 1.50 \
        sausage 3.00 \
        canadian bacon 3.50 \
        AI sauce 1.50 \
        peppers 1.00 \
        Drinks: \
        coke 3.00, 2.00, 1.00 \
        sprite 3.00, 2.00, 1.00 \
        bottled water 5.00 \
"""})
   
   

    await websocket.send_json(context)

    while "salir" not in prompt.lower():
        # Solicitar la orden del cliente

        prompt = await websocket.receive_text()
        print(prompt)

        # Agregar la respuesta del usuario al contexto
        context.append({"role": "user", "content": f"{prompt}"})

        # Generar una respuesta del bot en función del contexto actual
        response = get_completion_from_messages(context)
        print(response)

        # Agregar la respuesta del bot al contexto
        context.append({"role": "assistant", "content": f"{response}"})

        # Si el usuario ingresa "salir", generar el resumen de la orden
        if "salir"  in prompt.lower():
            # Agregar el mensaje al contexto para generar el resumen de la orden
            print("entro en el loop")
            context.append({"role": "system", "content": """
            Create a resume of the order.\
            Show it like a receipt of a restaurant. \
            The fields should be: \
            
            1) pizza, include size \
            1.1)Name of the Client \
            2) list of toppings \
            3) list of drinks, include size \
            5) total price
            """})

            # Generar la respuesta del bot con el resumen de la orden
            response = get_completion_from_messages(context)
            print(response)

            # Agregar la respuesta del bot al contexto
            context.append({"role": "assistant", "content": f"{response}"})

            # Guardar la última respuesta en un archivo JSON
            with open('summary.json', 'a') as f:
                json.dump(response, f)
                f.write("\n")

        # Guardar la conversación actual en el archivo JSON
        with open('data.json', 'a') as f:
            json.dump(context, f)
            f.write("\n")
            
        # Enviar la respuesta del bot al frontend
        await websocket.send_json(context)

@app.post("/post-audio-search-escrito")
async def post_audio(data:dict):

    message_decoded = data["question"]
    print(message_decoded)

    response = search(message_decoded)

    return {"response": response}

@app.post("/single_url_llama")
async def url(data:dict):

    liga = data["url"] 
    user = data["user"]
    load_url(liga=liga,user=user)

    return {"set"}

@app.post("/resumen_global_single")
async def url_resumen(data:dict):
    print(data)
    user = data["user"]
    response = pregunta_url_resumen(user=user)

    return {"response":response}

@app.post("/pregunta_single")
async def url_abierta(data:dict):
    print(data)
    user = data["user"]
    question = data["question"]
    response = pregunta_url_abierta(user=user,question=question)

    return {"response":response}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    chat_ids = cargar_chat_ids()
    data = await request.json()

    if "message" in data:
        message = data["message"]
        chat_id = message.get("chat", {}).get("id")
        print(chat_id)
        # Verificar si el chat_id existe en el diccionario
        if str(chat_id) in chat_ids:
            usuario = chat_ids[str(chat_id)]
        else:
            usuario = "error"
        print(usuario)

        if str(chat_id)  in authorized_users:
            if "text" in message:
                    message_decoded = message["text"]
                    print(message_decoded)

                    # Get chat response
                    chat_response = get_chat_response_telegram(message_decoded)
                    print(chat_response)
                    # Guard: Ensure output
                    if not chat_response:
                        raise HTTPException(status_code=400, detail="Failed chat response")

                    await bot.send_message(chat_id=chat_id,text=chat_response)
                    incrementar_contador_clicks(chat_id)
                    store_messages_telegram(request_message=message_decoded, response_message=chat_response,user=usuario)

                          
            elif "voice" in message:
                    audio_file_id = message["voice"]["file_id"]

                    # Obtener la URL de descarga del archivo de audio
                    get_path = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(token, audio_file_id))
                    json_doc = loads(get_path.text)
                    try:
                        file_path = json_doc['result']['file_path']
                        print(file_path)
                    except Exception as e:
                        print('No se puede descargar el archivo porque su tamaño supera los 20 MB')
                        return

                    file_url = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)

                    # Descargar el archivo de audio
                    response = requests.get(file_url)
                    print(response)
                    audio_data = response.content
                    with open("audio.oga", "wb") as file:
                        file.write(audio_data)
                    print("Archivo de audio descargado")

                # Convertir audio a un formato aceptado (por ejemplo, a WAV)
                    audio = AudioSegment.from_file("audio.oga", format="ogg", ffmpeg=ffmpeg_path)
                    audio.export("audio.wav", format="wav")

                    # Abrir y procesar el archivo de audio convertido
                    with open("audio.wav", "rb") as audio_file:
                        message_decoded = convert_audio_to_text(audio_file)
                        print(message_decoded)
                        print("Audio recibido (estructura de voz)")
                                # Get chat response
                    chat_response = get_chat_response_telegram(message_decoded)
                    print(chat_response)
                    store_messages_telegram(request_message=message_decoded, response_message=chat_response,user=usuario)

                    # Guard: Ensure output
                    if not chat_response:
                        raise HTTPException(status_code=400, detail="Failed chat response")


                    # Convert chat response to audio
                    audio_output = convert_text_to_speech_telegram(chat_response)

                    # Guard: Ensure output
                    if not audio_output:
                        raise HTTPException(status_code=400, detail="Failed audio output")

                    
                    # Guardar los bytes de audio en un archivo
                    with open("audio_output.ogg", "wb") as audio_file:
                        audio_file.write(audio_output)

                    ## Obtener la duración del audio en segundos
                    audio = AudioSegment.from_file("audio_output.ogg", ffmpeg=ffmpeg_path)
                    audio_duration_sec = len(audio) / 1000
                    print("Duración del audio:", audio_duration_sec, "segundos")

                    # Enviar el audio a través de Telegram
                    with open("audio_output.ogg", "rb") as audio_file:
                        response = await bot.send_voice(chat_id=chat_id, voice=audio_file, duration=audio_duration_sec)
                        incrementar_contador_clicks(chat_id)


                    # Verificar si el mensaje de voz fue enviado correctamente
                    if message is not None:
                        print("Audio enviado correctamente")
                    else:
                        print("No se pudo enviar el audio a través de Telegram")

            
            else:
                print("No se encuentra el campo 'message' en el objeto JSON")
        else:
            chat_response = "Acceso no autorizado. Contrata el servicio escribiendo a 0rland0.eth"

            # Verificar si el mensaje ya ha sido enviado
            if "message_sent" not in message:
                await bot.send_message(chat_id=chat_id, text=chat_response)

                # Actualizar el campo "message_sent" en el objeto "message"
                message["message_sent"] = True
                return {"message": "OK"}

            else:
                raise HTTPException(status_code=403, detail="Acceso no autorizado")

    return {"message": "OK"}



@app.on_event("startup")
async def setup_webhook():
    # Configurar el webhook con la API de Telegram
    webhook_endpoint = f"https://api.telegram.org/bot{token}/setWebhook"
    webhook_url = f"{ngrok_url}/webhook"
    # webhook_url = "https://readymad3.com/webhook"
    response = requests.post(webhook_endpoint, json={"url": webhook_url})
    print(response)
    
    if response.status_code == 429:
        # Si se recibe el código de estado 429, esperar gradualmente y volver a intentarlo
        wait_time = 1  # Tiempo inicial de espera en segundos
        max_retries = 5  # Número máximo de intentos
        retries = 0
        
        while response.status_code == 429 and retries < max_retries:
            print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            response = requests.post(webhook_endpoint, json={"url": webhook_url})
            wait_time *= 2  # Duplicar el tiempo de espera en cada intento
            retries += 1
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to set webhook")
    

@app.post("/vector_index")
async def vecto(data: dict):
    user = data["user"]
    response = vector_index(user)
    return {"response": response}

@app.post("/resumen_opcion")
async def vecto(data: dict):
    user = data["user"]
    user_selection= data["option"]
    response = resumen_opcion_multiple(user,user_selection)
    return {"response": response}

@app.post("/data_pregunta")
async def pregunta(data: dict):
    user = data["user"]
    question= data["question"]
    response = pregunta_data(user,question)
    return {"response": response}

@app.post("/borrar_conversaciones")
async def borrar(data: dict):
    user = data["user"]
    response = borrar_contenido(user)
    return {"response": response}


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
