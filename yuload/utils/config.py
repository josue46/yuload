"""Module de configuration pour Yuload"""

import os
import platform
from pathlib import Path
import sys


class Config:
    """Classe de configuration centralisée de l'application"""

    # Tous les fichiers de l'application sont stockés dans le répertoire utilisateur
    APP_DIR: Path = Path.home() / ".yuload"
    # Dossier pour les vidéos téléchargées
    DOWNLOAD_DIR: Path = APP_DIR / "downloads"
    # Dossier pour les fichiers journaux (logs)
    LOG_DIR: Path = APP_DIR / "logs"
    # Dossier pour les fichiers temporaires (vidéo/audio avant fusion)
    TEMP_DIR: Path = APP_DIR / "temp"

    @staticmethod
    def init_directories():
        """
        Crée les répertoires de l'application s'ils n'existent pas.
        Cette fonction est appelée au démarrage de l'application.
        """
        Config.APP_DIR.mkdir(parents=True, exist_ok=True)
        Config.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        Config.TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # CONFIGURATION DE L'INTERFACE
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    # Dimensions minimales pour permettre le redimensionnement
    MIN_WINDOW_WIDTH = 600
    MIN_WINDOW_HEIGHT = 400

    # THÈME SOMBRE MODERNE
    BG_PRIMARY: str = "#1e1e1e"  # Fond principal (très sombre)
    BG_SECONDARY: str = "#2d2d2d"  # Fond secondaire (pour les panneaux)
    BG_TERTIARY: str = "#3d3d3d"  # Fond tertiaire (pour les boutons inactifs)
    FG_PRIMARY: str = "#ffffff"  # Texte principal (blanc)
    FG_SECONDARY: str = "#a0a0a0"  # Texte secondaire (gris clair)
    ACCENT_COLOR: str = "#0078d4"  # Bleu Microsoft pour les éléments actifs
    ERROR_COLOR: str = "#f44747"  # Rouge pour les erreurs
    SUCCESS_COLOR: str = "#4ec9b0"  # Vert pour les succès
    WARNING_COLOR: str = "#dcdcaa"  # Jaune pour les avertissements

    # POLICES DE CARACTÈRES
    # Détection automatique : Segoe UI sur Windows, Ubuntu sur Linux
    FONT_FAMILY: str = "Segoe UI" if os.name == "nt" else "Ubuntu"
    FONT_SIZE_TITLE: int = 14  # Taille pour les titres
    FONT_SIZE_LABEL: int = 10  # Taille pour les étiquettes normales
    FONT_SIZE_SMALL: int = 9  # Taille pour le texte petit

    # PARAMÈTRES DE TÉLÉCHARGEMENT
    MAX_RETRIES: int = 3  # Nombre de tentatives en cas d'échec
    CHUNK_SIZE: int = 1024 * 1024  # Taille des chunks téléchargés (1 MB)
    # Qualités vidéo préférées (dans l'ordre de préférence)
    QUALITY_PREFERENCES: tuple[str] = ("1080p", "720p", "480p", "360p", "144p")

    # DÉLAIS D'EXPIRATION (TIMEOUTS)
    REQUEST_TIMEOUT = 10  # Délai pour les requêtes HTTP (10 secondes)
    DOWNLOAD_TIMEOUT = 300  # Délai pour les téléchargements (5 minutes)

    # CONFIGURATION DE FFMPEG
    # FFmpeg est utilisé ici pour fusionner vidéo et audio sans perte de qualité
    USE_FFMPEG_MERGE = True  # Activation de la fusion avec FFmpeg
    FFMPEG_PRESET = "copy"  # "copy" = ultra rapide, pas de réencodage
    FFMPEG_AUDIO_CODEC = "aac"  # Codec audio par défaut

    # INFORMATION SYSTÈME
    # Déterminer le système d'exploitation pour la compatibilité multiplateforme
    SYSTEM_PLATFORM: str = platform.system()
    IS_WINDOWS: bool = SYSTEM_PLATFORM == "Windows"
    IS_MACOS: bool = SYSTEM_PLATFORM == "Darwin"
    IS_LINUX: bool = SYSTEM_PLATFORM == "Linux"

    @staticmethod
    def get_temp_file_path(filename: str) -> Path:
        """
        Retourne le chemin complet pour un fichier temporaire multiplateforme.

        Args:
            filename: Nom du fichier temporaire

        Returns:
            Chemin complet du fichier temporaire
        """
        return Config.TEMP_DIR / filename

    @staticmethod
    def get_ffmpeg_path() -> str:
        """
        Récupère le chemin vers le binaire FFmpeg.
        Gère le cas 'Frozen' (PyInstaller) et le cas développement.
        """
        # Si l'application est empaquetée avec PyInstaller
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            ffmpeg_exe = "ffmpeg.exe" if Config.IS_WINDOWS else "ffmpeg"
            bundle_ffmpeg = Path(sys._MEIPASS) / ffmpeg_exe
            if bundle_ffmpeg.exists():
                return str(bundle_ffmpeg)

        try:
            import imageio_ffmpeg

            return imageio_ffmpeg.get_ffmpeg_exe()
        except (ImportError, RuntimeError):
            return "ffmpeg"

    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """
        Obtient le chemin absolu vers une ressource,
        fonctionne pour le dev et pour PyInstaller
        """
        try:
            # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
            base_path = Path(sys._MEIPASS)
        except Exception:
            # En mode développement, on utilise le chemin relatif classique
            base_path = Path(os.path.abspath("."))

        return base_path / relative_path
