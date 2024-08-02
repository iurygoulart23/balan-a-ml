# Scrapper do Mercado Livre
Autor: Iury Goulart

## Projeto para adquirir dados do Mercado Livre para pegar produtos piratas

O codigo consiste em:
1 - scrapper_ml entra no site do Mercado Livre, faz a pesquisa do termo que vc gostaria
    traz os itens da pesquisa e salva em JSON na pasta downloads
2 - O modelo GPT 3.5 faz a analise do produto e a classifica como realmente o produto buscado
    ou se é apenas um acessório para o produto. (podendo descartar o que não é necessário)
3 - Cruza com os dados do site do INMETRO para ver se a marca já tem o registro desse produto.

Foi utilizado `python 3.10.14` 

### Bibliotecas usadas:
- beautifulsoup4
- numpy
- Pillow
- selenium
- webdriver_manager
- json
- openai

*Gastos com GPT 3.5 Turbo 16k - localização canada east*

- input 240 tokens por item
- output 150  tokens por item
```
input $0.0005
1000 tokens 

output 	$0.0015
1000 tokens
```

CUSTO ESTIMADO
- input 6 dolares/página
- output 11,25 dolares/pagina