import requests
from decouple import config


ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

import requests

url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
  "xi-api-key": ELEVEN_LABS_API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

voices = data["voices"]

for voice in voices:
    name = voice["name"]
    voice_id = voice["voice_id"]
    print("Name:", name)
    print("Voice ID:", voice_id)
    print("---")


# ---
# Name: belinda test
# Voice ID: k6ySAJf7wfnoqjacH1BJ
# ---