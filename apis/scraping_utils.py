import requests
from bs4 import BeautifulSoup
import re

class ScrapingUtils:
    """
    Classe utilitária para realizar scraping em sites e extrair informações relevantes.
    """

    @staticmethod
    def get_html_content(url):
        """
        Faz uma requisição HTTP para uma URL e retorna o conteúdo HTML.
        :param url: URL do site que será acessado.
        :return: Conteúdo HTML da página.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao acessar a URL {url}: {e}")
            return None

    @staticmethod
    def extract_text_from_html(html_content):
        """
        Extrai o texto limpo de um conteúdo HTML utilizando o BeautifulSoup.
        :param html_content: Conteúdo HTML bruto.
        :return: Texto limpo extraído da página.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()  # Remove scripts e estilos para manter o texto limpo
            text = soup.get_text(separator=' ')
            text = re.sub(r'\s+', ' ', text).strip()  # Remove múltiplos espaços e formata o texto
            return text
        except Exception as e:
            print(f"Erro ao extrair texto do HTML: {e}")
            return None

    @staticmethod
    def search_in_html(html_content, query):
        """
        Busca uma palavra-chave ou expressão no conteúdo HTML e retorna os trechos que contêm a palavra-chave.
        :param html_content: Conteúdo HTML da página.
        :param query: Palavra-chave ou expressão a ser buscada.
        :return: Lista de trechos de texto que contêm a palavra-chave.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator=' ')
            matches = [match.group(0) for match in re.finditer(rf"\b{re.escape(query)}\b", text, re.IGNORECASE)]
            return matches
        except Exception as e:
            print(f"Erro ao buscar palavra-chave no HTML: {e}")
            return []

    @staticmethod
    def extract_links_from_html(html_content):
        """
        Extrai todos os links (URLs) de uma página HTML.
        :param html_content: Conteúdo HTML da página.
        :return: Lista de URLs presentes na página.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return links
        except Exception as e:
            print(f"Erro ao extrair links do HTML: {e}")
            return []

    @staticmethod
    def extract_metadata_from_html(html_content):
        """
        Extrai metadados (como título, descrições) de uma página HTML.
        :param html_content: Conteúdo HTML da página.
        :return: Dicionário contendo metadados como título e descrição.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            metadata = {}
            metadata['title'] = soup.title.string if soup.title else 'Sem título'
            metadata['description'] = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'Sem descrição'
            return metadata
        except Exception as e:
            print(f"Erro ao extrair metadados do HTML: {e}")
            return {}

