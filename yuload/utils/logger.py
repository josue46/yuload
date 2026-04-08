"""Module de logging pour Yuload"""

import logging
import logging.handlers
from datetime import datetime
from .config import Config


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Configure un logger avec des handlers fichier et console
    
    Args:
        name: Nom du logger
        log_file: Nom du fichier log optionnel
        
    Returns:
        Instance du logger configurée
    """
    # Création du logger avec le niveau DEBUG pour capturer tous les messages
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Éviter les handlers dupliqués si la fonction est appelée plusieurs fois
    if logger.handlers:
        return logger
    
    # Format des messages logs : timestamp - nom - niveau - message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler console : affiche les logs à la console (niveau INFO minimum)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Crer le répertoire des logs s'il n'existe pas
    # Ceci est essentiel car le logger au niveau module tente de créer un fichier avant init_directories()
    Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Nom du fichier log (par défaut : yuload_YYYYMMDD.log)
    if log_file is None:
        log_file = f"yuload_{datetime.now().strftime('%Y%m%d')}.log"
    
    log_path = Config.LOG_DIR / log_file
    
    # Handler fichier : écrit les logs dans un fichier avec rotation automatique
    # maxBytes=10MB : le fichier est archivé quand il atteint 10MB
    # backupCount=5 : on garde les 5 derniers fichiers archivés
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=1024*1024*10,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Créer le logger par défaut au chargement du module
# Ce logger enregistrera tous les événements de l'application
logger = setup_logger(__name__)
