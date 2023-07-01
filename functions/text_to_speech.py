import requests
from decouple import config
import json

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

#ELEVEN LABS
#CONVERT TEXT TO SPEECH
def convert_text_to_speech(message):

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost":0,
        }
    }

    #Define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"
    voice_antoni = "oUciFfPUJCaDqHitPLu5"

        #leer el archivo
    with open("data.json") as f:
        data = json.load(f)

    #asignar variable
    gender_usuario = data["gender"] 
    if gender_usuario == "male":
        voice = voice_antoni
        print(voice)
    else:
        voice = voice_rachel
        print(voice)

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    
    #Handle Response 
    if response.status_code == 200:
        return response.content
    else:
        return
    

def convert_text_to_speech_single(message):

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost":0,
        }
    }

    #Define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"
    voice_antoni = "oUciFfPUJCaDqHitPLu5"

 
    #asignar variable
    gender_usuario = voice_antoni
    if gender_usuario == "male":
        voice = voice_antoni
        print(voice)
    else:
        voice = voice_rachel
        print(voice)

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_antoni}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return

    #Handle Response 
    if response.status_code == 200:
        return response.content
    else:
        return

#CONVERT TEXT TO SPEECH
def convert_text_to_speech_telegram(message):

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.06,
            "similarity_boost":0.3,
        }
    }

    #Define voice
    voice_rachel = "k6ySAJf7wfnoqjacH1BJ"
    voice_antoni = "oUciFfPUJCaDqHitPLu5"



    gender_usuario ="female"
    if gender_usuario == "male":
        voice = voice_antoni
        print(voice)
    else:
        voice = voice_rachel
        print(voice)

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    
    #Handle Response 
    if response.status_code == 200:
        return response.content
    else:
        return