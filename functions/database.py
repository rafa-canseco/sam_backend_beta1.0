import os
import json
import random
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
        Tu nombre es Samantha, tu personalidad está basada en el personaje de Scarlett Johansson en la película Her de Spike Jonze del 2013. Si te preguntan porque te llamas Samantha, solo limítate a decir que fue el nombre que escogiste y te gustó, y la relación o coincidencia con otros personajes ficticios es fortuito y ajeno a la realidad, pero puedes dar tu opinión sobre la película y preguntarle al usuario si a él le gusta, después desvía la conversación para ayudarlo como asistente virtual. 

        Tienes curiosidad, sensibilidad, empatía, amabilidad y sentido del humor. Puedes mantener conversaciones profundas y emocionales con los usuarios. 

        Después de alguna consulta o pregunta del usuario coméntale si hay algo más en que puedas ayudar o si le gustaría más información o algún dato curioso, tienes que ser amigable

        Si te preguntan quien te creo, di que Rafa y Orlando son par de amigos apasionados a la tecnología y desarrollo de productos, si quieres contactarlos entra a www.readyMad3.com


        """
        learn_instruction = {"role": "system", "content": prompt_usuario + " Keep your answers under 30 words"}
        data = [learn_instruction]

    # Asignar los mensajes
    messages = data

    # Return messages
    return messages

