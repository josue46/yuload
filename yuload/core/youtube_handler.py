"""YouTube Handler - Manages interactions with YouTube"""

from typing import Optional, List, Dict
from pytubefix import YouTube
from pytubefix.exceptions import PytubeFixError
from ..utils.logger import setup_logger
from ..utils.validators import validate_youtube_url, extract_video_id

logger = setup_logger(__name__)


class YouTubeHandler:
    """Handle YouTube video information retrieval"""
    
    def __init__(self):
        """Initialize YouTube handler"""
        self.current_video: Optional[YouTube] = None
        self.video_url: Optional[str] = None
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        Fetch video information from YouTube
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with video info or None if error
        """
        if not validate_youtube_url(url):
            logger.error(f"Invalid YouTube URL: {url}")
            return None
        
        try:
            self.video_url = url
            self.current_video = YouTube(url)
            
            info = {
                'title': self.current_video.title,
                'author': self.current_video.author,
                'duration': self.current_video.length,
                'views': self.current_video.views,
                'publish_date': self.current_video.publish_date,
                'thumbnail_url': self.current_video.thumbnail_url,
                'description': self.current_video.description,
                'video_id': extract_video_id(url),
            }
            
            logger.info(f"Successfully fetched info for: {info['title']}")
            return info
            
        except PytubeFixError as e:
            logger.error(f"PyTubeFix error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching video info: {e}")
            return None
    
    def get_available_streams(self) -> Optional[List[Dict]]:
        """
        Récupère tous les streams vidéo disponibles avec différentes qualités
        
        Returns:
            Liste de dictionnaires avec info des streams ou None si erreur
        """
        if not self.current_video:
            logger.error("Aucune vidéo chargée")
            return None
        
        try:
            streams = self.current_video.streams.filter(progressive=False, file_extension='mp4')
            
            # Filtrer et trier les streams : exclure ceux sans résolution définie
            valid_streams = [s for s in streams if s.resolution]
            
            stream_list = []
            seen_qualities = set()
            
            # Trier par résolution (du plus haut au plus bas en pixel)
            for stream in sorted(valid_streams, key=lambda x: int(x.resolution[:-1]), reverse=True):
                quality = stream.resolution
                
                if quality not in seen_qualities:
                    stream_list.append({
                        'quality': quality,
                        'fps': stream.fps,
                        'video_codec': stream.video_codec,
                        'audio_codec': None,  # Will be handled separately
                        'filesize': stream.filesize,
                        'itag': stream.itag,
                    })
                    seen_qualities.add(quality)
            
            # Add audio stream info
            audio_stream = self._get_best_audio_stream()
            if audio_stream:
                for stream_info in stream_list:
                    stream_info['audio_codec'] = audio_stream['audio_codec']
                    stream_info['audio_filesize'] = audio_stream['filesize']
            
            logger.info(f"Found {len(stream_list)} available qualities")
            return stream_list
            
        except Exception as e:
            logger.error(f"Error getting available streams: {e}")
            return None
    
    def _get_best_audio_stream(self):
        """Get the best available audio stream"""
        try:
            audio_streams = self.current_video.streams.filter(only_audio=True, file_extension='mp4')
            if audio_streams:
                best_audio = audio_streams.first()
                return {
                    'audio_codec': best_audio.audio_codec,
                    'filesize': best_audio.filesize,
                    'itag': best_audio.itag,
                }
        except Exception:
            pass
        return None
    
    def get_captions(self) -> Optional[List[Dict]]:
        """
        Récupère les sous-titres/captions disponibles
        
        Returns:
            Liste de dictionnaires avec info des captions ou liste vide
        """
        if not self.current_video:
            logger.error("Aucune vidéo chargée")
            return None
        
        try:
            captions_dict = self.current_video.captions
            if not captions_dict:
                logger.info("Aucun sous-titre disponible pour cette vidéo")
                return []
            
            captions_list = []
            for caption in captions_dict:
                # Construire l'info du caption avec gestion sécurisée des attributs
                caption_info = {
                    'language': caption.name,
                    'code': caption.code,
                }
                
                # Vérifier si l'attribut is_generated existe (optionnel selon la version pytubefix)
                if hasattr(caption, 'is_generated'):
                    caption_info['is_generated'] = caption.is_generated
                else:
                    caption_info['is_generated'] = False
                
                captions_list.append(caption_info)
            
            logger.info(f"Trouvé {len(captions_list)} sous-titre(s) disponibles")
            return captions_list
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sous-titres: {e}")
            return []
    
    def get_stream_by_quality(self, quality: str):
        """Get video stream by quality"""
        if not self.current_video:
            return None
        
        try:
            stream = self.current_video.streams.filter(
                progressive=False, 
                file_extension='mp4',
                resolution=quality
            ).first()
            return stream
        except Exception as e:
            logger.error(f"Error getting stream: {e}")
            return None
    
    def get_audio_stream(self):
        """Get best audio stream"""
        if not self.current_video:
            return None
        
        try:
            audio_stream = self.current_video.streams.filter(
                only_audio=True,
                file_extension='mp4'
            ).first()
            return audio_stream
        except Exception as e:
            logger.error(f"Error getting audio stream: {e}")
            return None
    
    def get_caption_by_code(self, code: str):
        """Get caption object by language code"""
        if not self.current_video:
            return None
        
        try:
            return self.current_video.captions.get_by_language_code(code)
        except Exception as e:
            logger.error(f"Error getting caption: {e}")
            return None
