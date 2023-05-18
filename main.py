# uvicorn main:app
# uvicorn main:app --reload



# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException,WebSocket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from typing import Dict
import json
import uvicorn




# Custom function imports
from functions.text_to_speech import convert_text_to_speech, convert_text_to_speech_single
from functions.openai_requests import convert_audio_to_text, get_chat_response, get_chat_response_simple
from functions.database import store_messages, reset_messages, store_messages_simple
from functions.newAdd import instruction,search, youtube_resume, pdf_pages, dirty_data,abstraction, blockchain_tx,url_resume, preguntar_url, preguntar_youtube
from functions.completion import get_completion_from_messages



# Get Environment Vars
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Initiate App
app = FastAPI()


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
async def Ask_pdf(data: dict):
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
async def Ask_pdf(data: dict):
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

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
