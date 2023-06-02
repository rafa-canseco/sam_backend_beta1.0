import openai 
from decouple import config
from functions.database import get_recent_messages,get_recent_messages_simple,get_recent_messages_telegram


#retrieve our eviroment variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

#open ai -whisper
#convert audio to text

def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return
    
#Open AI - CHATGPT
#Get response to our message
def get_chat_response(message_input):

    messages = get_recent_messages()
    user_messages = {"role":"user","content":message_input}
    messages.append(user_messages)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(e)
        return
    
def get_chat_response_simple(message_input):

    messages = get_recent_messages_simple()
    user_messages = {"role":"user","content":message_input}
    messages.append(user_messages)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(e)
        return
    
def get_chat_response_telegram(message_input):
    print("función     1")
    messages = get_recent_messages_telegram()
    user_messages = {"role":"user","content":message_input}
    messages.append(user_messages)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(e)
        return