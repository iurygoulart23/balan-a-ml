# Databricks notebook source
import pandas as pd
import openai
import json
from dotenv import find_dotenv, load_dotenv
import os
import logging

# config logging
log_file_path = '../logs/openai_gpt.log'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# abre variaveis de ambiente
load_dotenv(find_dotenv())

# endpoint e modelo
model_engine = os.getenv("MODEL_ENGINE")
openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")
openai.api_version = os.getenv("API_VERSION")

# COMMAND ----------

# prompt
context = 'Você é um analista de produtos do INMETRO, precisa analisar informações textuais de balanças para conseguir identificar o que é uma balança e o que não é. Também precisa identificar a informação da Marca da balança e separar a informação da Marca em uma resposta em JSON. As informações que você deverá analisar estão em formato de JSON dentro de uma array abaixo, você deve procurar o nome da marca dentro das chaves "brand" e "product_name" e me retornar APENAS um novo JSON com as mesmas chaves e valores anteriores porém com mais duas chaves "balança": True ou False e "marca": "nome da marca": '

# pega o json balanças
with open('../downloads/balança.json', 'r') as f:
  x = f.read()

descricoes = json.loads(x)

count = 0

# itera nos itens do json de balanças
for descricao in descricoes[:2]:
  
  if ("Balança" in descricao['product_name']) | ("BALANÇA" in descricao['product_name']):
  
    prompt  = context + "'" + str(descricao) + "'"

    # print(prompt)

    # cria o payload para o openai
    try:
      response = openai.ChatCompletion.create(
      model="gpt35-turbo",
      messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": f"{descricao}"}
      ],
      deployment_id = "gpt4",
      max_tokens = 1000,
      stop = None,
      temperature = 0,
      )

      model_response = response.choices[0].message.content
      print(model_response)

      with open('../downloads/answers_gpt.txt', 'a') as f:
        f.write(model_response)
        f.write('\n')

    except Exception as e:
      print(f"Ocorreu um erro: {e}")

# deployment_id  = 'gpt4',


# COMMAND ----------

descricoes[:20]