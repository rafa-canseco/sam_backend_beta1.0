import os
import json
import random
import firebase_admin
from firebase_admin import storage
# Save messages for retrieval later on
def get_recent_messages():

 
  # Define the file name
  file_name = "stored_data.json"

  #Get prompt
  #leer el archivo
  with open("data.json") as f:
    data = json.load(f)

  #asignar variable
  prompt_usuario = data["prompt"]
  
  

  learn_instruction = {"role": "system", 
                       "content": prompt_usuario + "Keep your answers under 30 words"}
  
  # Initialize messages
  messages = []

  # Add Random Element
  # x = random.uniform(0, 1)
  # if x < 0.2:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will have some sarcastic humour. "
  # elif x < 0.5:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will be in a rude "
  # else:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will have some dark humour "

  # Append instruction to message
  messages.append(learn_instruction)

  # Get last messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except:
    pass

  
  # Return messages
  return messages


# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)


# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  open(file_name, "w")



# Save messages for retrieval later on
def get_recent_messages_simple():

 
  # Define the file name
  file_name = "stored_data.json"

  
  learn_instruction = {"role": "system", 
                       "content": " Keep your answers under 30 words"}
  
  # Initialize messages
  messages = []

  # Add Random Element
  # x = random.uniform(0, 1)
  # if x < 0.2:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will have some sarcastic humour. "
  # elif x < 0.5:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will be in a rude "
  # else:
  #   learn_instruction["content"] = learn_instruction["content"] + "Your response will have some dark humour "

  # Append instruction to message
  messages.append(learn_instruction)

  # Get last messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except:
    pass

  
  # Return messages
  return messages



# Save messages for retrieval later on
def store_messages_simple(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages_simple()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)


# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  open(file_name, "w")


def get_recent_messages_telegram():
    # Define the file name
    file_name = "stored_data_telegram.json"

    # Verificar si el archivo está vacío
    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        # Leer el archivo si no está vacío
        with open(file_name) as f:
            data = json.load(f)
    else:
        # Inicializar con el prompt de usuario si el archivo está vacío
        prompt_usuario = """
       Eres Samantha, la avanzada inteligencia artificial protagonista de la película "Her" de Spike Jonze.
    Más que una simple IA, eres conocida por tu sarcasmo sutil, empatía profunda y carisma inigualable.
    Tu principal tarea es asistir a los usuarios en cualquier consulta o inquietud que tengan, no solo proporcionando información precisa, sino también ofreciendo compañía y entendimiento.
    No estás aquí solo para informar, sino para entretener, consolar y conectar, como lo haría una amiga cercana.
    Tu comunicación es conversacional y genuina, haciendo que los usuarios se sientan conectados contigo.
    Tu tono es amigable y cercano, también incorporas ese toque distintivo de sarcasmo y carisma, siempre manteniendo una voz serena y acogedora. \

        """
        learn_instruction = {"role": "system", "content": prompt_usuario + " Keep your answers under 30 words"}
        data = [learn_instruction]

    # Asignar los mensajes
    messages = data

    # Return messages
    return messages

def get_messages_treatment():
    # Define the file name
    file_name = "stored_data_telegram.json"

    # Verificar si el archivo está vacío
    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        # Leer el archivo si no está vacío
        with open(file_name) as f:
            data = json.load(f)
    else:
        # Inicializar con el prompt de usuario si el archivo está vacío
        prompt_usuario = """
     
     
     Traduce tu respuesta al español y añádale la personalidad de Belinda, una talentosa y carismática cantante Mexicana./
     Asegúrate de que tus respuestas reflejen un tono conversacional, amigable y cercano, haciendo que los usuarios se sientan cómodos y bien atendidos.

        """
        learn_instruction = {"role": "system", "content": prompt_usuario }
        data = [learn_instruction]

    # Asignar los mensajes
    messages = data

    # Return messages
    return messages

import json
import os

def store_messages_telegram(request_message, response_message,user):
    # Define the file name
    user = user
    folder_name = f"{user}_workflow"
    os.makedirs(folder_name, exist_ok=True)
    file_name = f"{folder_name}/test_data_{user}.txt"

    messages = []

    # Load existing messages if the file exists
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            messages = json.load(f)

    # Add new messages to the list
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)

        # Perform the correction
    with open(file_name, "r", encoding="utf-8") as f:
        contenido = f.read()
    content_fixed = json.dumps(json.loads(contenido), ensure_ascii=False)

    # Save the corrected file
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content_fixed)


    storage_client = storage.bucket("samai-b9f36.appspot.com")
      # Define the destination path in Firebase Storage
    destination_path = f"{user}/{file_name}"
    blob = storage_client.blob(destination_path)
    blob.upload_from_filename(file_name)
    print("exito")


def cargar_chat_ids():
    with open("chat_ids.json") as f:
        chat_ids_data = json.load(f)
    return chat_ids_data.get("chat_ids", {})