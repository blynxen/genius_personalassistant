import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class SafetyAgent:
    """
    Agente especializado em consultas sobre Segurança do Trabalho e Meio Ambiente.
    Usa scraping e Selenium com Microsoft Edge para buscar informações atualizadas.
    """

    def __init__(self):
        """
        Inicializa o agente de segurança do trabalho e meio ambiente com o Microsoft Edge.
        """
        self.base_url_nrs = "https://www.gov.br/trabalho-e-previdencia/pt-br/assuntos/seguranca-e-saude-no-trabalho/normas-regulamentadoras"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Configurações do Microsoft Edge
        edge_options = Options()
        edge_options.use_chromium = True
        edge_options.add_argument("--headless")  # Executar em segundo plano (sem abrir o navegador)
        edge_options.add_argument("--disable-gpu")  # Desativar GPU para melhor desempenho
        edge_options.add_argument("--no-sandbox")
        
        # Localização do WebDriver do Edge (certifique-se de que o caminho esteja correto)
        self.driver_path = r"D:\Personal_Assistent\data\msedgedriver.exe"  # Ajuste o caminho para o WebDriver do Edge
        
        # Inicializa o driver do Microsoft Edge
        self.driver = webdriver.Edge(service=Service(self.driver_path), options=edge_options)

    def search_safety_law(self, query):
        """
        Faz a busca de informações sobre segurança do trabalho e meio ambiente usando Microsoft Edge.
        :param query: Termo de busca relacionado a segurança ou meio ambiente.
        :return: Lista de resultados encontrados.
        """
        search_url = f"{self.base_url_nrs}/search?SearchableText={query}"
        try:
            self.driver.get(search_url)
            return self._parse_search_results_selenium()
        except Exception as e:
            return f"Erro ao realizar a busca no Edge: {str(e)}"

    def _parse_search_results_selenium(self):
        """
        Usa Selenium para processar os resultados da página carregada no Edge.
        :return: Lista de normas encontradas.
        """
        results = []
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.summary.url")
            for element in elements:
                title = element.text
                link = element.get_attribute('href')
                results.append({"title": title, "link": link})

            return results if results else "Nenhuma norma encontrada para a consulta."
        except Exception as e:
            return f"Erro ao processar os resultados com Selenium: {str(e)}"

    def search_by_nr_number(self, nr_number):
        """
        Busca uma NR específica (Norma Regulamentadora) diretamente na internet.
        :param nr_number: Número da NR (e.g., "NR-12", "NR-35").
        :return: Informação sobre a NR encontrada.
        """
        nr_url = f"{self.base_url_nrs}/normas/{nr_number.lower()}"
        try:
            self.driver.get(nr_url)
            return self._parse_nr_details_selenium()
        except Exception as e:
            return f"Erro ao buscar NR no Edge: {str(e)}"

    def _parse_nr_details_selenium(self):
        """
        Faz o parsing dos detalhes de uma NR específica (Norma Regulamentadora) usando Selenium.
        :return: Informações detalhadas sobre a NR.
        """
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.documentFirstHeading").text
            description = self.driver.find_element(By.CSS_SELECTOR, "div.documentDescription").text
            url = self.driver.current_url

            return {"title": title, "description": description, "url": url}
        except Exception as e:
            return f"Erro ao buscar detalhes da NR: {str(e)}"

    def search_latest_updates(self):
        """
        Faz a busca por atualizações recentes de normas de segurança e regulamentações ambientais.
        :return: Lista de normas ou regulamentações mais recentes encontradas.
        """
        try:
            self.driver.get(self.base_url_nrs)
            return self._parse_latest_updates_selenium()
        except Exception as e:
            return f"Erro ao buscar atualizações no Edge: {str(e)}"

    def _parse_latest_updates_selenium(self):
        """
        Faz o parsing das atualizações mais recentes de normas regulamentadoras e segurança.
        :return: Lista de atualizações mais recentes.
        """
        try:
            updates = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.summary.url")
            for element in elements:
                title = element.text
                link = element.get_attribute('href')
                updates.append({"title": title, "link": link})

            return updates if updates else "Nenhuma atualização recente encontrada."
        except Exception as e:
            return f"Erro ao processar as atualizações com Selenium: {str(e)}"

    def close(self):
        """
        Fecha o navegador Microsoft Edge após o uso.
        """
        self.driver.quit()
