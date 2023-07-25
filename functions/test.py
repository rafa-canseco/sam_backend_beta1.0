# from decouple import config
# from langchain.chat_models import ChatOpenAI
# import os
# import pandas as pd
# from langchain.agents import (
#     load_tools,
#     initialize_agent,
#     create_pandas_dataframe_agent,
#     Tool,
#     AgentType,
# )
# import matplotlib.pyplot as plt
# from pandasai import PandasAI
# import os
# from langchain.agents import create_sql_agent
# from langchain.sql_database import SQLDatabase


# os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
# llm = ChatOpenAI(model ="gpt-3.5-turbo",temperature =0)
# df = pd.read_csv("ds_salaries.csv")


# pandas_ai = PandasAI(llm,verbose=False)
# # query="cuantas columnas y filas hay?"
# # query="cual es el salario promedio de un AI developer?"
# # query="grafica los 5 trabajos que tengan en promedio el mejor salario"
# query="haz un pie chart con los porcentajes mayor a 1% de las ubicaciones de las compañías"

# pandas_ai(df,query)
# respuesta = pandas_ai(df,query)

# print("----------------")
# print(respuesta)
# print("----------------")


# #####

# db_user = "db_user"
# db_password = "db_password"
# db_host = "db_host"
# db_name = "db_name"
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


# from langchain.chat_models import ChatOpenAI
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# toolkit = SQLDatabase(db=db)
# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True
# )

# agent_executor.run("Describe the Order related table and how they are related")



count = 0

for number in range(1, 904):
    if number % 3 == 0:
        count += 1

print(count)
