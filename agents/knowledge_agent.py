import os
import fitz  # PyMuPDF para PDF parsing
import docx  # python-docx para arquivos DOCX
import textract  # Para extração de texto de vários formatos
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

class KnowledgeAgent:
    """
    Agente especializado em consultas de bases de conhecimento locais e no MongoDB.
    """

    def __init__(self, knowledge_base_dir="D:/Personal_Assistent/data/knowlegde_base"):
        """
        Inicializa o agente com as configurações de base de conhecimento local e MongoDB.
        :param knowledge_base_dir: Diretório onde os arquivos locais da base de conhecimento estão armazenados.
        """
        self.knowledge_base_dir = knowledge_base_dir
        
        # Configurações do MongoDB
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_db = os.getenv("MONGO_DB_NAME")
        self.mongo_collection = os.getenv("MONGO_COLLECTION_NAME")

        # Verificar se as variáveis de ambiente são válidas
        if not all([self.mongo_uri, self.mongo_db, self.mongo_collection]):
            raise ValueError("Verifique se todas as variáveis de ambiente do MongoDB estão configuradas corretamente")

        try:
            # Conectar ao MongoDB
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.collection = self.db[self.mongo_collection]
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao MongoDB: {e}")

    def search_mongo(self, query):
        """
        Faz uma consulta na base de conhecimento no MongoDB.
        :param query: Consulta do usuário.
        :return: Lista de documentos relevantes encontrados.
        """
        try:
            mongo_query = {"$text": {"$search": query}}  # Usar pesquisa full-text no MongoDB
            results = self.collection.find(mongo_query)
            return [doc for doc in results]  # Retorna uma lista de documentos encontrados
        except Exception as e:
            return [f"Erro ao consultar MongoDB: {str(e)}"]

    def search_local_knowledge(self, query):
        """
        Faz a busca em arquivos locais da base de conhecimento. Suporta múltiplos formatos de arquivos (PDF, DOCX, TXT).
        :param query: Consulta do usuário.
        :return: Resultados encontrados nos arquivos locais.
        """
        results = []
        for file in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, file)
            if file.endswith('.pdf'):
                results.extend(self._search_in_pdf(file_path, query))
            elif file.endswith('.docx'):
                results.extend(self._search_in_docx(file_path, query))
            elif file.endswith('.txt'):
                results.extend(self._search_in_txt(file_path, query))
            else:
                print(f"Formato de arquivo {file} não suportado.")
        return results

    def _search_in_pdf(self, file_path, query):
        """
        Faz a busca por palavras-chave em arquivos PDF.
        :param file_path: Caminho do arquivo PDF.
        :param query: Consulta do usuário.
        :return: Lista de ocorrências encontradas.
        """
        results = []
        try:
            with fitz.open(file_path) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    text = page.get_text("text")
                    if query.lower() in text.lower():
                        results.append(f"Encontrado no arquivo {file_path}, página {page_num + 1}.")
        except Exception as e:
            print(f"Erro ao processar PDF {file_path}: {e}")
        return results

    def _search_in_docx(self, file_path, query):
        """
        Faz a busca por palavras-chave em arquivos DOCX.
        :param file_path: Caminho do arquivo DOCX.
        :param query: Consulta do usuário.
        :return: Lista de ocorrências encontradas.
        """
        results = []
        try:
            doc = docx.Document(file_path)
            for i, para in enumerate(doc.paragraphs):
                if query.lower() in para.text.lower():
                    results.append(f"Encontrado no arquivo {file_path}, parágrafo {i + 1}.")
        except Exception as e:
            print(f"Erro ao processar DOCX {file_path}: {e}")
        return results

    def _search_in_txt(self, file_path, query):
        """
        Faz a busca por palavras-chave em arquivos TXT.
        :param file_path: Caminho do arquivo TXT.
        :param query: Consulta do usuário.
        :return: Lista de ocorrências encontradas.
        """
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f.readlines()):
                    if query.lower() in line.lower():
                        results.append(f"Encontrado no arquivo {file_path}, linha {i + 1}.")
        except Exception as e:
            print(f"Erro ao processar TXT {file_path}: {e}")
        return results

    def search_knowledge_base(self, query):
        """
        Faz a busca na base de conhecimento, tanto no MongoDB quanto em arquivos locais.
        :param query: Consulta do usuário.
        :return: Resultados encontrados na base de conhecimento.
        """
        results = []

        # Primeiro, tenta buscar no MongoDB
        if self.client:
            mongo_results = self.search_mongo(query)
            if mongo_results:
                results.extend(mongo_results)

        # Se não houver resultados ou se o MongoDB não estiver configurado, busca em arquivos locais
        if not results:
            local_results = self.search_local_knowledge(query)
            results.extend(local_results)

        if results:
            return results
        else:
            return "Nenhuma informação encontrada para a consulta."
