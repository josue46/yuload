"""Module de configuration pour Yuload"""

import os
from pathlib import Path


class Config:
    """Classe de configuration centralisée de l'application"""
    
    # ======================== RÉPERTOIRES DE BASE ========================
    # Tous les fichiers de l'application sont stockés dans le répertoire utilisateur
    APP_DIR = Path.home() / ".yuload"
    # Dossier pour les vidéos téléchargées
    DOWNLOAD_DIR = APP_DIR / "downloads"
    # Dossier pour les fichiers journaux (logs)
    LOG_DIR = APP_DIR / "logs"
    
    @staticmethod
    def init_directories():
        """
        Crée les répertoires de l'application s'ils n'existent pas.
        Cette fonction doit être appelée au démarrage de l'application.
        """
        Config.APP_DIR.mkdir(parents=True, exist_ok=True)
        Config.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # ======================== CONFIGURATION DE L'INTERFACE ========================
    # Dimensions de la fenêtre principale (largeur x hauteur en pixels)
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    # Dimensions minimales pour permettre le redimensionnement
    MIN_WINDOW_WIDTH = 600
    MIN_WINDOW_HEIGHT = 400
    
    # ======================== THÈME SOMBRE MODERNE ========================
    # Tous les codes hexadécimaux utilisés dans TOUTE l'interface
    BG_PRIMARY = "#1e1e1e"       # Fond principal (très sombre)
    BG_SECONDARY = "#2d2d2d"     # Fond secondaire (pour les panneaux)
    BG_TERTIARY = "#3d3d3d"      # Fond tertiaire (pour les boutons inactifs)
    FG_PRIMARY = "#ffffff"        # Texte principal (blanc)
    FG_SECONDARY = "#a0a0a0"     # Texte secondaire (gris clair)
    ACCENT_COLOR = "#0078d4"     # Bleu Microsoft pour les éléments actifs
    ERROR_COLOR = "#f44747"      # Rouge pour les erreurs
    SUCCESS_COLOR = "#4ec9b0"    # Vert pour les succès
    WARNING_COLOR = "#dcdcaa"    # Jaune pour les avertissements
    
    # ======================== POLICES DE CARACTÈRES ========================
    # Détection automatique : Segoe UI sur Windows, Ubuntu sur Linux
    FONT_FAMILY = "Segoe UI" if os.name == "nt" else "Ubuntu"
    FONT_SIZE_TITLE = 14      # Taille pour les titres
    FONT_SIZE_LABEL = 10      # Taille pour les étiquettes normales
    FONT_SIZE_SMALL = 9       # Taille pour le texte petit
    
    # ======================== PARAMÈTRES DE TÉLÉCHARGEMENT ========================
    MAX_RETRIES = 3            # Nombre de tentatives en cas d'échec
    CHUNK_SIZE = 1024 * 1024   # Taille des chunks téléchargés (1 MB)
    # Qualités vidéo préférées (dans l'ordre de préférence)
    QUALITY_PREFERENCES = ["1080p", "720p", "480p", "360p", "144p"]
    
    # ======================== DÉLAIS D'EXPIRATION (TIMEOUTS) ========================
    REQUEST_TIMEOUT = 10       # Délai pour les requêtes HTTP (10 secondes)
    DOWNLOAD_TIMEOUT = 300     # Délai pour les téléchargements (5 minutes)
