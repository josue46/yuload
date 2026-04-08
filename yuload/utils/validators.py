"""Utilitaires de validation pour Yuload"""

import os
import re
from pathlib import Path


def validate_youtube_url(url: str) -> bool:
    """
    Valide si l'URL est une URL YouTube valide.
    Accepte les variantes : youtube.com, youtu.be, youtube-nocookie.com
    
    Args:
        url: URL à valider
        
    Returns:
        True si l'URL est valide, False sinon
    """
    # Regex pour détecter les variantes YouTube
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    )
    
    url = url.strip()
    # Ajouter https:// si pas de protocole
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return bool(re.match(youtube_regex, url))


def validate_output_path(path: str) -> bool:
    """
    Valide si le chemin de sortie est valide et accessible en écriture.
    Crée le répertoire parent s'il n'existe pas.
    
    Args:
        path: Chemin à valider
        
    Returns:
        True si valide et accessible, False sinon
    """
    try:
        path_obj = Path(path)
        
        # Créer le répertoire parent s'il n'existe pas
        if not path_obj.parent.exists():
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Vérifier que c'est un répertoire et qu'on a les droits d'écriture
        return path_obj.parent.is_dir() and os.access(path_obj.parent, os.W_OK)
    except (OSError, ValueError):
        return False


def extract_video_id(url: str) -> str:
    """
    Extrait l'ID vidéo YouTube de l'URL.
    Fonctionne avec youtube.com, youtu.be et les formats embed.
    
    Args:
        url: URL YouTube
        
    Returns:
        ID vidéo ou chaîne vide si non trouvé
    """
    # Deux patterns pour couvrir les différents formats YouTube
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ""
