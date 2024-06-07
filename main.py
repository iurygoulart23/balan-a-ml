from myFunctions.navegador import navegador_firefox
from myFunctions.arrumaScrapper import tempo_espera_aleatorio
import ssl
import subprocess

class Scrapper:
    def __init__(self, url, buscar, headless=True, install_firefox=True, salvar_pagina=False, imprimir=False):
        if install_firefox:
            bash_script_path = './assets/installFirefox.sh'
            subprocess.run(['bash', bash_script_path], capture_output=True, text=True)

        ssl._create_default_https_context = ssl._create_unverified_context

        self.headless = headless
        self.buscar = buscar
        self.url = url
        self.links = []
        self.imprimir = imprimir
        self.driver = navegador_firefox(headless)
        self.salvar_pagina = salvar_pagina
    
    def navega(self):
        
        self.driver.get(self.url)
        
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        
        with open('assets/search.js', 'r') as f:
            js_code = f.read()
        
        self.driver.execute_script(js_code)

    def fecha_navegador(self):
        self.driver.quit()

    def get_data(self) -> list:

        from selenium.webdriver.common.by import By

        results = self.driver.find_elements(By.CSS_SELECTOR, 'div.ui-search-result__wrapper')
        resultados = [i.text for i in results]
        
        return resultados
    
    def troca_pag(self):

        from selenium.webdriver.common.by import By

        # Localizar o elemento que contém o link para a próxima página
        next_page_element = self.driver.find_element(By.CSS_SELECTOR, 'li.andes-pagination__button--next a')
        
        # Obter o valor do atributo href do elemento
        next_page_link = next_page_element.get_attribute('href')
        
        # Clicar no link para a próxima página
        self.driver.get(next_page_link)

        return
    
    def get_next_pag_link(self) -> str:
        
        

        return next_page_link

    def parse_results_to_json(self, results, pag):
        
        import re
        import json
        
        structured_data = []

        for result in results:
            # Initialize a dictionary to store the product data
            product_data = {}
            
            # Split the result by new lines and iterate over the parts
            parts = result.split('\n')
            product_data['brand'] = parts[0]
            product_data['product_name'] = parts[1]
            
            # Extract price and discount information
            price_match = re.search(r'R\$\n(\d+)\n,\n(\d+)', result)
            if price_match:
                product_data['price'] = f"{price_match.group(1)}.{price_match.group(2)}"
            
            # Check for original price and discount
            original_price_match = re.search(r'R\$\n(\d+)\n,\n(\d+)\n(\d+)% OFF', result)
            if original_price_match:
                product_data['original_price'] = f"{original_price_match.group(1)}.{original_price_match.group(2)}"
                product_data['discount'] = original_price_match.group(3)
            
            # Extract rating and opinions
            rating_match = re.search(r'Avaliação (\d+\.\d+) de 5\. (\d+) opiniões\.', result)
            if rating_match:
                product_data['rating'] = rating_match.group(1)
                product_data['opinions'] = rating_match.group(2)
            
            # Check for free shipping
            product_data['free_shipping'] = 'Frete grátis' in result
            
            # Check for multiple colors
            product_data['multiple_colors'] = 'Disponível em' in result
            
            # Add the product data to the structured data list
            structured_data.append(product_data)
        
        if self.imprimir:
            print(json.dumps(structured_data, indent=4))

        # Convert the structured data to JSON
        with open(f"./downloads/{self.buscar}_pag{pag}.json", "w") as f:
            f.write(json.dumps(structured_data, indent=4))
        
        return structured_data


if __name__ == "__main__":

    link = "https://www.mercadolivre.com.br/"
    buscar = "balança"

    scrapper = Scrapper(url=link,
                        headless=False,
                        install_firefox=False,
                        salvar_pagina=False,
                        buscar='balança',
                        imprimir=True)
    
    scrapper.navega()

    tempo_espera_aleatorio(low=2, high=3)

    for pag in range(0, 10):

        results = scrapper.get_data()
        results_json = scrapper.parse_results_to_json(results, pag)

        scrapper.troca_pag()
        tempo_espera_aleatorio(low=2, high=4)


    scrapper.fecha_navegador()