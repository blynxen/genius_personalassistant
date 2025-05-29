import ollama
from utils.moderation import ContentModeration
from agents.knowledge_agent import KnowledgeAgent



class GeniusAgent:
    def __init__(self, ollama_model="geniusv1:latest", knowledge_base_agent=None):
        """
        Inicializa o agente com o modelo Ollama e opcionalmente um agente de base de conhecimento.
        :param ollama_model: Nome do modelo Ollama a ser usado.
        :param knowledge_base_agent: Agente responsável por consultas na base de conhecimento local (MongoDB).
        """
        self.ollama_model = ollama_model  # Nome do modelo Ollama
        self.client = ollama.Client()  # Cliente Ollama para uso local
        self.knowledge_base_agent = knowledge_base_agent  # Agente de base de conhecimento (opcional)
        self.content_moderation = ContentModeration()  # Inicializa a moderação de conteúdo

    def query(self, input_text):
        """
        Processa a consulta, verificando primeiro a base de conhecimento e depois consultando o modelo LLM.
        :param input_text: Texto da pergunta feita pelo usuário.
        :return: Resposta gerada pelo agente.
        """
        # Verifica se o texto contém conteúdo inapropriado
        if self.content_moderation.contains_inappropriate_content(input_text):
            return "Desculpe, não posso responder a essa solicitação por conter conteúdo inapropriado."

        # Primeiro, tenta consultar na base de conhecimento (MongoDB ou arquivos locais) se houver um knowledge_base_agent
        if self.knowledge_base_agent:
            print("Consultando base de conhecimento local...")
            knowledge_base_response = self.knowledge_base_agent.search_local_knowledge(input_text)
            if knowledge_base_response:
                return knowledge_base_response

        # Se a base de conhecimento local não tiver uma resposta, consulta o modelo Ollama
        print("Consultando modelo Ollama local...")
        return self.query_llm(input_text)

    def query_llm(self, input_text):
        """
        Faz uma consulta ao modelo Ollama localmente.
        :param input_text: Texto da pergunta feita pelo usuário.
        :return: Resposta gerada pelo modelo.
        """
        try:
            # Faz a consulta ao modelo usando o cliente Ollama
            response = self.client.chat(
                model=self.ollama_model,
                messages=[{'role': 'user', 'content': input_text}]
            )
            return response["message"]["content"]  # Retorna a resposta gerada pelo modelo
        except Exception as e:
            return f"Erro ao consultar o modelo Ollama: {e}"

    def moderate_and_query(self, input_text):
        """
        Modera o texto, remove conteúdo inapropriado, e faz a consulta ao LLM ou à base de conhecimento.
        :param input_text: Texto da pergunta feita pelo usuário.
        :return: Resposta gerada pelo agente.
        """
        moderated_text = self.content_moderation.moderate_content(input_text)

        # Após a moderação, verifica se o texto moderado ainda contém conteúdo e faz a consulta
        if moderated_text:
            return self.query(moderated_text)
        else:
            return "O conteúdo da sua mensagem foi removido por conter informações inapropriadas."
