import logging
from logging.handlers import RotatingFileHandler
import os

# Cria diretório de logs, caso não exista
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuração padrão do arquivo de log
LOG_FILE = os.path.join(LOG_DIR, "genius.log")
LOG_LEVEL = logging.DEBUG  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)

def setup_logger():
    """
    Configura o logger para o agente, utilizando um sistema de logs rotativos
    e níveis de log configuráveis.
    """
    logger = logging.getLogger("DmGeniusLogger")
    logger.setLevel(LOG_LEVEL)

    # Configura um RotatingFileHandler para o arquivo de log
    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=5 * 1024 * 1024,  # Máximo de 5MB por arquivo de log
        backupCount=3  # Mantém 3 backups (ex: genius.log.1, genius.log.2)
    )
    
    # Definição do formato de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Adiciona o handler ao logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Instancia o logger
logger = setup_logger()

def log_debug(message):
    """
    Registra mensagens de debug.
    """
    logger.debug(message)

def log_info(message):
    """
    Registra mensagens de informação.
    """
    logger.info(message)

def log_warning(message):
    """
    Registra mensagens de alerta.
    """
    logger.warning(message)

def log_error(message):
    """
    Registra mensagens de erro.
    """
    logger.error(message)

def log_critical(message):
    """
    Registra mensagens críticas.
    """
    logger.critical(message)
