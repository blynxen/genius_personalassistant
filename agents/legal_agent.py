import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


class LegalAgent:
    """
    Agente especializado em consultas sobre legislação, jurisprudência e documentos legais.
    Faz consultas ao portal LexML para buscar informações atualizadas.
    """

    def __init__(self):
        """
        Inicializa o agente jurídico configurado para realizar buscas no portal LexML.
        """
        self.base_url = "http://www.lexml.gov.br/busca/search"
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

    def search_legal_documents(self, query):
        """
        Faz uma busca de documentos legais no portal LexML.
        :param query: Termo de busca (por exemplo: "lei da liberdade econômica").
        :return: Lista de resultados de documentos legais.
        """
        search_url = f"{self.base_url}?q={query}"
        try:
            response = requests.get(search_url, headers=self.headers)
            if response.status_code == 200:
                return self._parse_search_results(response.content)
            else:
                return f"Erro ao acessar o LexML. Código de status: {response.status_code}"
        except Exception as e:
            return f"Erro ao realizar a busca no LexML: {str(e)}"

    def _parse_search_results(self, html_content):
        """
        Faz o parsing dos resultados da busca no LexML.
        :param html_content: Conteúdo HTML da página de resultados.
        :return: Lista de documentos legais encontrados.
        """
        soup = BeautifulSoup(html_content, 'lxml')
        results = []
        
        # Busca pelos elementos que contêm os títulos e links dos documentos
        documents = soup.find_all("div", class_="resultado-busca")
        
        for doc in documents:
            try:
                title = doc.find("a").get_text(strip=True)
                link = doc.find("a")['href']
                date = doc.find("span", class_="data").get_text(strip=True)
                
                # Verifica se o link é absoluto ou relativo e ajusta
                if not link.startswith("http"):
                    link = f"http://www.lexml.gov.br{link}"
                
                results.append({
                    "title": title,
                    "link": link,
                    "date": date
                })
            except AttributeError:
                continue  # Ignora entradas mal formatadas

        return results if results else "Nenhum documento encontrado para a consulta."

    def get_legal_document_details(self, document_url):
        """
        Faz o scraping dos detalhes de um documento legal específico no LexML.
        :param document_url: URL do documento no portal LexML.
        :return: Detalhes do documento legal.
        """
        try:
            response = requests.get(document_url, headers=self.headers)
            if response.status_code == 200:
                return self._parse_document_details(response.content)
            else:
                return f"Erro ao acessar o documento no LexML. Código de status: {response.status_code}"
        except Exception as e:
            return f"Erro ao acessar o documento no LexML: {str(e)}"

    def _parse_document_details(self, html_content):
        """
        Faz o parsing dos detalhes de um documento legal específico.
        :param html_content: Conteúdo HTML da página do documento.
        :return: Detalhes do documento legal.
        """
        soup = BeautifulSoup(html_content, 'lxml')
        try:
            title = soup.find("h1", class_="titulo-documento").get_text(strip=True)
            summary = soup.find("div", class_="resumo").get_text(strip=True)
            date = soup.find("span", class_="data").get_text(strip=True)
            return {
                "title": title,
                "summary": summary,
                "date": date
            }
        except AttributeError:
            return "Erro ao obter os detalhes do documento."

    def search_legislation_by_year(self, year):
        """
        Busca por leis específicas em um ano.
        :param year: Ano de interesse (por exemplo: 2023).
        :return: Lista de documentos legais encontrados.
        """
        search_url = f"{self.base_url}?q=ano:{year}"
        try:
            response = requests.get(search_url, headers=self.headers)
            if response.status_code == 200:
                return self._parse_search_results(response.content)
            else:
                return f"Erro ao acessar o LexML. Código de status: {response.status_code}"
        except Exception as e:
            return f"Erro ao realizar a busca por ano no LexML: {str(e)}"
