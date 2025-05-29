import requests
from bs4 import BeautifulSoup

class DataGovernanceAgent:
    """
    Agente especializado em governança de dados, segurança da informação e regulamentações como LGPD, GDPR, e CCPA.
    """

    def __init__(self):
        """
        Inicializa o agente com URLs ou fontes para scraping.
        """
        self.sources = {
            'lgpd': "https://www.gov.br/secretariageral/pt-br/lgpd",  # Site oficial do governo brasileiro sobre LGPD
            'gdpr': "https://gdpr-info.eu",                            # Base de dados online sobre GDPR
            'ccpa': "https://oag.ca.gov/privacy/ccpa"                  # Site oficial da Califórnia sobre CCPA
        }

    def query_laws(self, region, query):
        """
        Faz a consulta de leis de governança de dados via scraping nos sites oficiais.
        :param region: Região ou país a ser consultado (e.g., 'lgpd', 'gdpr', 'ccpa').
        :param query: Termo ou tópico relacionado a governança de dados (e.g., 'tratamento de dados').
        :return: Resposta formatada com informações sobre a lei consultada.
        """
        if region in self.sources:
            return self._scrape_law_info(self.sources[region], query, region.upper())
        else:
            return f"Região não reconhecida: {region}. Por favor, escolha entre 'lgpd', 'gdpr', ou 'ccpa'."

    def _scrape_law_info(self, url, query, law_name):
        """
        Realiza scraping no site oficial para obter informações relevantes com base na consulta.
        :param url: URL do site a ser consultado.
        :param query: Termo ou tópico a ser pesquisado.
        :param law_name: Nome da regulamentação a ser consultada (e.g., LGPD, GDPR).
        :return: Resposta formatada com os resultados encontrados.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Simplesmente coletar todo o texto da página
            page_text = soup.get_text().lower()

            # Verificar se a consulta está contida no texto da página
            if query.lower() in page_text:
                return f"Informação encontrada sobre '{query}' na página de {law_name}. Acesse diretamente: {url}"
            else:
                return f"Nenhuma informação específica sobre '{query}' encontrada em {law_name}. Acesse para mais detalhes: {url}"
        except requests.RequestException as e:
            return f"Erro ao consultar {law_name}: {e}"

