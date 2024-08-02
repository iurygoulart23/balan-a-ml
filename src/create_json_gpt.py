def create_json_from_gpt():
  """Cria um JSON a partir das respostas do modelo da OpenAI"""

  with open('./downloads/answers_gpt.txt', 'r') as f:
    respostas_json = f.read()

  # trata os valores recebidos da OpenAi
  try:
    new_list = []
    for i in respostas_json.split('```json')[1:]:
      item = i.replace('```', '').replace('\n', '').replace('  ', ' ').replace(' "brand"', '"brand"')
      item = item.replace('True', 'true').replace('False', 'false')  # Correct boolean values

      new_list.append(item)
      chama = json.loads(item)

      print(chama)
  except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {chama}")
          
  # Converter as strings JSON em objetos Python
  produtos = [json.loads(resposta) for resposta in new_list]

  # Salvar a lista de produtos em um arquivo JSON
  with open('produtos.json', 'w', encoding='utf-8') as arquivo_json:
      json.dump(produtos, arquivo_json, ensure_ascii=False, indent=4)
  
  return print("Os produtos foram salvos com sucesso no arquivo 'produtos.json'.")

