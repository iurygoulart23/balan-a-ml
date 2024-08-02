from myFunctions.navegador import navegador_firefox
from myFunctions.arrumaScrapper import tempo_espera_aleatorio
import ssl
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Scrapper:
    def __init__(self, url, buscar, headless=True, install_firefox=True, salvar_pagina=False, imprimir=False):
        if install_firefox:
            bash_script_path = '../assets/installFirefox.sh'
            subprocess.run(['bash', bash_script_path], capture_output=True, text=True)

        ssl._create_default_https_context = ssl._create_unverified_context

        self.headless = headless
        self.buscar = buscar
        self.url = url
        self.imprimir = imprimir
        self.driver = navegador_firefox(headless)
        self.salvar_pagina = salvar_pagina
    
    def enter_website(self):
        
        self.driver.get(self.url)
        tempo_espera_aleatorio(low=2, high=3)
        return

    def select_instrumento(self):

        sel_instrumento = "sel_tipo_instrumento_medida"
        
        javascript = f"""
            // Find the select element by its name attribute
            // const selectName = "sel_tipo_instrumento_medida";
            const selectElement = document.querySelector(`[name="${sel_instrumento}"]`);

            // Select an option by its value
            selectElement.value = "1-Balança";

            // Find the input element with name "descr_marca" and send keys
            const marcaInput = document.querySelector('[name="descr_marca"]');
            marcaInput.value = "{self.buscar}";
        """

        select = Select(self.driver.find_element(By.NAME, sel_instrumento))

        # select by value 
        select.select_by_value('1-Balança')

        self.driver.find_element(By.NAME, "descr_marca").send_keys(self.buscar)

        self.driver.find_element(By.NAME, "btnPesquisar").click()

        tempo_espera_aleatorio(low=2, high=3)

        return


    def navega(self):
        
        self.driver.get(self.url)
        
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        
        with open('../assets/search.js', 'r') as f:
            js_code = f.read()
        
        self.driver.execute_script(js_code)


    def fecha_navegador(self):
        self.driver.quit()
        return
    
    def verify_product(self):

        # tem que ter mais de 4 resultados
        trs = self.driver.find_elements(By.TAG_NAME, 'tr')

        if len(trs) >= 6 :
            return True
        else:
            return False


if __name__ == "__main__":

    link = "http://www.inmetro.gov.br/legislacao/consulta.asp?seq_classe=2"
    marca = "iphone"

    scrapper = Scrapper(url=link,
                        headless=False,
                        install_firefox=False,
                        salvar_pagina=False,
                        buscar=marca,
                        imprimir=True)
    
    scrapper.enter_website()

    scrapper.select_instrumento()

    print(f'O produto "{marca}" se encaixa como: {scrapper.verify_product()}')

    # results = scrapper.get_data()
    # results_json = scrapper.parse_results_to_json(results, pag)

    # scrapper.troca_pag()
    # tempo_espera_aleatorio(low=2, high=4)


    scrapper.fecha_navegador()