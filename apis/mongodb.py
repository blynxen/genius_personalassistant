from pymongo import MongoClient
from config.config import Config

class MongoDBAgent:
    """
    Agente responsável pela conexão e interação com o MongoDB.
    Pode ser usado para buscar dados na base de conhecimento armazenada no MongoDB.
    """

    def __init__(self):
        """
        Inicializa o agente e estabelece a conexão com o MongoDB.
        """
        try:
            # Conexão com o MongoDB
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DB_NAME]
            self.collection = self.db[Config.MONGO_COLLECTION_NAME]
            print(f"Conectado ao MongoDB: {Config.MONGO_URI}")
        except Exception as e:
            print(f"Erro ao conectar no MongoDB: {e}")

    def search_in_knowledge_base(self, query):
        """
        Pesquisa na base de conhecimento (MongoDB) usando uma palavra-chave ou frase.

        :param query: Termo de busca (string) fornecido pelo usuário.
        :return: Lista de resultados que correspondem à pesquisa.
        """
        try:
            search_results = self.collection.find({"$text": {"$search": query}})
            results = []

            # Coleta os resultados da consulta
            for result in search_results:
                results.append({
                    "title": result.get("title", "Sem título"),
                    "content": result.get("content", "Sem conteúdo"),
                    "source": result.get("source", "Desconhecido")
                })

            if results:
                return results
            else:
                return ["Nenhuma correspondência encontrada na base de conhecimento."]
        except Exception as e:
            return [f"Erro ao buscar na base de conhecimento: {e}"]

    def insert_document(self, document):
        """
        Insere um novo documento na coleção de base de conhecimento.

        :param document: Dicionário contendo as chaves "title", "content", e "source".
        :return: Confirmação da inserção.
        """
        try:
            result = self.collection.insert_one(document)
            return f"Documento inserido com o ID: {result.inserted_id}"
        except Exception as e:
            return f"Erro ao inserir o documento: {e}"

    def close_connection(self):
        """
        Fecha a conexão com o MongoDB.
        """
        self.client.close()
        print("Conexão com o MongoDB fechada.")
