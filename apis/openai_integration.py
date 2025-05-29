import openai
import os
from config.config import Config

class OpenAIIntegration:
    """
    Agente responsável pela integração com a API da OpenAI.
    Pode ser usado para consultas que envolvam processamento de linguagem natural ou busca de informações contextuais.
    """

    def __init__(self):
        """
        Inicializa o agente e configura a chave da API da OpenAI a partir do arquivo de configuração.
        """
        openai.api_key = Config.OPENAI_API_KEY  # Chave da API da OpenAI, carregada do arquivo de configuração

    def query_openai(self, prompt, model="gpt-4", max_tokens=300):
        """
        Envia uma consulta (prompt) para a API da OpenAI e recebe uma resposta gerada pelo modelo.

        :param prompt: Texto ou pergunta enviada para a OpenAI.
        :param model: Modelo a ser utilizado na geração da resposta. (Padrão: gpt-4)
        :param max_tokens: Número máximo de tokens permitidos na resposta.
        :return: Resposta gerada pela OpenAI.
        """
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                n=1,
                stop=None
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erro ao consultar a API da OpenAI: {e}"

    def query_chat(self, messages, model="gpt-4"):
        """
        Envia uma sequência de mensagens para a API da OpenAI e recebe uma resposta em formato de chat.

        :param messages: Lista de mensagens no formato [{'role': 'user', 'content': 'Pergunta'}]
        :param model: Modelo de chat a ser utilizado (padrão: gpt-4).
        :return: Resposta gerada pela OpenAI no formato de chat.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Erro ao consultar a API de chat da OpenAI: {e}"
