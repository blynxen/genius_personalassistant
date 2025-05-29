import requests
import json
import os

class WebSearchAgent:
    def __init__(self):
        # Carrega as chaves de API e URLs a partir das variáveis de ambiente
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_cx = os.getenv('GOOGLE_CX')  # ID do mecanismo de pesquisa personalizada do Google

    def query_web(self, query, use_tavily=True, use_google=False, use_news=False):
        """
        Faz uma busca na web utilizando Tavily, Google ou outras APIs.
        :param query: A consulta a ser realizada
        :param use_tavily: Se deve usar Tavily API
        :param use_google: Se deve usar Google Custom Search API
        :param use_news: Se deve buscar em notícias (opcional)
        :return: Resposta da pesquisa em forma de texto
        """
        if use_tavily and self.tavily_api_key:
            return self._search_tavily(query)
        elif use_google and self.google_api_key and self.google_cx:
            return self._search_google(query)
        else:
            return "Nenhuma fonte de pesquisa válida disponível ou configurada."

    def _search_tavily(self, query):
        """
        Busca informações usando a Tavily API.
        :param query: A consulta de pesquisa
        :return: Resultado da pesquisa ou mensagem de erro
        """
        try:
            url = f"https://api.tavily.com/search?q={query}"
            headers = {"Authorization": f"Bearer {self.tavily_api_key}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return self._format_tavily_response(data)
            else:
                return f"Erro ao consultar Tavily: {response.status_code}"
        except Exception as e:
            return f"Erro na integração com Tavily: {e}"

    def _format_tavily_response(self, data):
        """
        Formata a resposta da API Tavily em um formato legível.
        :param data: Dados JSON retornados pela Tavily API
        :return: Texto formatado da resposta
        """
        try:
            results = data.get('results', [])
            if not results:
                return "Nenhum resultado encontrado na Tavily."

            response_text = "Resultados da pesquisa Tavily:\n"
            for result in results:
                title = result.get('title', 'Sem título')
                link = result.get('link', 'Sem link')
                snippet = result.get('snippet', 'Sem descrição')
                response_text += f"**{title}**\n{snippet}\nLink: {link}\n\n"
            return response_text
        except Exception as e:
            return f"Erro ao formatar a resposta da Tavily: {e}"

    def _search_google(self, query):
        """
        Faz a busca usando o Google Custom Search API.
        :param query: A consulta de pesquisa
        :return: Resultado da pesquisa ou mensagem de erro
        """
        try:
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.google_cx}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return self._format_google_response(data)
            else:
                return f"Erro ao consultar Google Search: {response.status_code}"
        except Exception as e:
            return f"Erro na integração com Google Search: {e}"

    def _format_google_response(self, data):
        """
        Formata a resposta da Google Custom Search API.
        :param data: Dados JSON retornados pela Google API
        :return: Texto formatado da resposta
        """
        try:
            items = data.get('items', [])
            if not items:
                return "Nenhum resultado encontrado no Google Search."

            response_text = "Resultados da pesquisa Google Search:\n"
            for item in items:
                title = item.get('title', 'Sem título')
                link = item.get('link', 'Sem link')
                snippet = item.get('snippet', 'Sem descrição')
                response_text += f"**{title}**\n{snippet}\nLink: {link}\n\n"
            return response_text
        except Exception as e:
            return f"Erro ao formatar a resposta do Google Search: {e}"

