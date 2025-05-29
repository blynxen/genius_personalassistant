import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Classe de configuração central do sistema. Todas as variáveis de configuração e de ambiente são
    carregadas e centralizadas aqui.
    """

    # Caminhos de diretórios principais
    KNOWLEDGE_BASE_DIR = os.getenv('KNOWLEDGE_BASE_DIR', 'D:/Personal_Assistent/data/knowledge_base')
    AUDIO_DIR = os.getenv('AUDIO_DIR', 'D:/Personal_Assistent/data/audio_responses')
    IMAGE_OUTPUT_DIR = os.getenv('IMAGE_OUTPUT_DIR', 'D:/Personal_Assistent/data/image_responses')

    # Configuração de modelos
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'geniusv1:latest')
    TTS_MODEL = os.getenv('TTS_MODEL', 'tts_models/multilingual/multi-dataset/xtts_v2')
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'small')

    # Configuração do MongoDB
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'genius_database')
    MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME', 'knowledge_base')

    # Moderação de conteúdo
    MODERATION_ENABLED = os.getenv('MODERATION_ENABLED', 'True') == 'True'

    # Configurações de APIs Externas
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', '')
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')

    # Variáveis de Ambiente para OpenAI e Tavily
    USE_TAVILY = os.getenv('USE_TAVILY', 'True') == 'True'
    USE_GOOGLE_SEARCH = os.getenv('USE_GOOGLE_SEARCH', 'False') == 'True'
    USE_NEWS_API = os.getenv('USE_NEWS_API', 'False') == 'True'

    # Parâmetros de Performance
    USE_GPU = os.getenv('USE_GPU', 'True') == 'True'  # Habilita ou desabilita o uso de GPU

    # Logger
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

    @staticmethod
    def show_config():
        """
        Exibe todas as variáveis de configuração carregadas, útil para depuração.
        """
        print("=== CONFIGURAÇÕES DO SISTEMA ===")
        print(f"KNOWLEDGE_BASE_DIR: {Config.KNOWLEDGE_BASE_DIR}")
        print(f"AUDIO_DIR: {Config.AUDIO_DIR}")
        print(f"IMAGE_OUTPUT_DIR: {Config.IMAGE_OUTPUT_DIR}")
        print(f"OLLAMA_MODEL: {Config.OLLAMA_MODEL}")
        print(f"TTS_MODEL: {Config.TTS_MODEL}")
        print(f"WHISPER_MODEL: {Config.WHISPER_MODEL}")
        print(f"MONGO_URI: {Config.MONGO_URI}")
        print(f"MONGO_DB_NAME: {Config.MONGO_DB_NAME}")
        print(f"MONGO_COLLECTION_NAME: {Config.MONGO_COLLECTION_NAME}")
        print(f"MODERATION_ENABLED: {Config.MODERATION_ENABLED}")
        print(f"OPENAI_API_KEY: {Config.OPENAI_API_KEY}")
        print(f"GOOGLE_API_KEY: {Config.GOOGLE_API_KEY}")
        print(f"GOOGLE_CSE_ID: {Config.GOOGLE_CSE_ID}")
        print(f"TAVILY_API_KEY: {Config.TAVILY_API_KEY}")
        print(f"USE_TAVILY: {Config.USE_TAVILY}")
        print(f"USE_GOOGLE_SEARCH: {Config.USE_GOOGLE_SEARCH}")
        print(f"USE_NEWS_API: {Config.USE_NEWS_API}")
        print(f"USE_GPU: {Config.USE_GPU}")
        print(f"LOG_LEVEL: {Config.LOG_LEVEL}")
