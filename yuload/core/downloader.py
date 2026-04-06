"""Module de téléchargement - Gère le téléchargement réel des vidéos"""

import os
import subprocess
from pathlib import Path
from typing import Callable, Optional
import threading
import time

from ..utils.logger import setup_logger
from ..utils.config import Config
from .youtube_handler import YouTubeHandler

logger = setup_logger(__name__)


class Downloader:
    """Gère le téléchargement de vidéos YouTube avec fusion audio/vidéo"""
    
    def __init__(self, youtube_handler: YouTubeHandler):
        """
        Initialise le téléchargeur
        
        Args:
            youtube_handler: Instance YouTubeHandler
        """
        self.handler = youtube_handler
        self.is_downloading = False
        self.current_thread: Optional[threading.Thread] = None
        # Références aux fichiers temporaires pour nettoyage
        self.temp_files = []
    
    def download_video(
        self,
        quality: str,
        output_path: str,
        include_subtitle: bool = False,
        subtitle_code: Optional[str] = None,
        progress_callback: Optional[Callable] = None,
        completion_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        status_callback: Optional[Callable] = None,
    ) -> bool:
        """
        Télécharge une vidéo dans un thread séparé
        
        Args:
            quality: Qualité vidéo (ex: "720p")
            output_path: Chemin du répertoire de sortie
            include_subtitle: Inclure les sous-titres
            subtitle_code: Code de langue pour les sous-titres
            progress_callback: Callback pour la progression
            completion_callback: Callback au téléchargement complet
            error_callback: Callback pour les erreurs
            status_callback: Callback pour les mises à jour de statut
            
        Returns:
            True si le téléchargement a démarré, False sinon
        """
        if self.is_downloading:
            error_msg = "Un téléchargement est déjà en cours"
            logger.warning(error_msg)
            if error_callback:
                error_callback(error_msg)
            return False
        
        # Démarrer le téléchargement dans un thread séparé (ne pas bloquer Tkinter)
        self.is_downloading = True
        self.current_thread = threading.Thread(
            target=self._download_video_thread,
            args=(
                quality,
                output_path,
                include_subtitle,
                subtitle_code,
                progress_callback,
                completion_callback,
                error_callback,
                status_callback,
            ),
            daemon=True
        )
        self.current_thread.start()
        return True
    
    def _download_video_thread(
        self,
        quality: str,
        output_path: str,
        include_subtitle: bool,
        subtitle_code: Optional[str],
        progress_callback: Optional[Callable],
        completion_callback: Optional[Callable],
        error_callback: Optional[Callable],
        status_callback: Optional[Callable],
    ):
        """Télécharge la vidéo dans un thread séparé"""
        try:
            # Valider et créer le répertoire de sortie
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Utiliser TEMP_DIR pour les fichiers temporaires
            temp_dir = Config.TEMP_DIR
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Obtenir les informations vidéo
            video_info = self.handler.current_video
            safe_title = self._make_safe_filename(video_info.title)
            
            # ÉTAPE 1: Télécharger le flux vidéo (sans audio)
            self._update_status(status_callback, "Téléchargement de la vidéo...")
            logger.info(f"Démarrage du téléchargement vidéo: {quality}")
            
            video_stream = self.handler.get_stream_by_quality(quality)
            if not video_stream:
                raise ValueError(f"Impossible de trouver un stream pour la qualité {quality}")
            
            # Wrapper pour convertir progression 0-33%
            def video_progress_wrapper(current, total):
                progress_ratio = (current / total) * 33 if total > 0 else 0
                if progress_callback:
                    progress_callback(progress_ratio, 100)
            
            video_file = self._download_stream(
                video_stream,
                temp_dir,
                f"{safe_title}_video.mp4",
                video_progress_wrapper,
                "vidéo"
            )
            
            if not video_file:
                raise Exception("Échec du téléchargement vidéo")
            
            self.temp_files.append(video_file)
            
            # ÉTAPE 2: Télécharger le flux audio (meilleure qualité)
            self._update_status(status_callback, "Téléchargement de l'audio...")
            logger.info("Démarrage du téléchargement audio")
            
            audio_stream = self.handler.get_audio_stream()
            if not audio_stream:
                raise Exception("Impossible de trouver un flux audio")
            
            # Wrapper pour convertir progression 33-66%
            def audio_progress_wrapper(current, total):
                progress_ratio = 33 + ((current / total) * 33) if total > 0 else 33
                if progress_callback:
                    progress_callback(progress_ratio, 100)
            
            audio_file = self._download_stream(
                audio_stream,
                temp_dir,
                f"{safe_title}_audio.mp4",
                audio_progress_wrapper,
                "audio"
            )
            
            if not audio_file:
                raise Exception("Échec du téléchargement audio")
            
            self.temp_files.append(audio_file)
            
            # ÉTAPE 3: Fusionner vidéo et audio avec FFmpeg
            self._update_status(status_callback, "Finalisation de la conversion vidéo...")
            logger.info("Fusion vidéo et audio avec FFmpeg")
            
            # Wrapper pour convertir progression 66-100% pendant fusion
            def merge_progress_wrapper(progress_pct):
                merge_progress = 66 + (progress_pct * 0.34)  # 66% à 100%
                if progress_callback:
                    progress_callback(merge_progress, 100)
            
            final_file = self._merge_with_ffmpeg(
                video_file,
                audio_file,
                output_dir,
                safe_title,
                merge_progress_wrapper
            )
            
            if not final_file:
                raise Exception("Échec de la fusion audio/vidéo")
            
            # ÉTAPE 4: Télécharger les sous-titres si demandé
            if include_subtitle and subtitle_code:
                self._update_status(status_callback, "Téléchargement des sous-titres...")
                logger.info(f"Téléchargement des sous-titres: {subtitle_code}")
                self._download_subtitle(
                    subtitle_code,
                    output_dir,
                    safe_title
                )
            
            # Succès - set to 100%
            if progress_callback:
                progress_callback(100, 100)
            
            # Nettoyer les fichiers temporaires et appeler le callback
            self._cleanup_temp_files()
            logger.info(f"Téléchargement complété: {final_file}")
            
            if completion_callback:
                completion_callback(final_file)
            
        except Exception as e:
            error_msg = f"Erreur de téléchargement: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Nettoyer en cas d'erreur
            self._cleanup_temp_files()
            
            if error_callback:
                error_callback(error_msg)
        
        finally:
            self.is_downloading = False
    
    def _update_status(self, status_callback: Optional[Callable], message: str):
        """Appelle le callback de statut si défini"""
        if status_callback:
            try:
                status_callback(message)
            except Exception as e:
                logger.error(f"Erreur dans le callback de statut: {e}")
    
    def _download_stream(
        self,
        stream,
        output_dir: Path,
        filename: str,
        progress_callback: Optional[Callable],
        stream_type: str = "vidéo"
    ) -> Optional[str]:
        """
        Télécharge un flux (vidéo ou audio) avec callback de progression
        
        Args:
            stream: Objet stream pytubefix
            output_dir: Répertoire de sortie
            filename: Nom du fichier de sortie
            progress_callback: Callback pour la progression
            stream_type: Type de stream ("vidéo" ou "audio") pour le logging
            
        Returns:
            Chemin du fichier ou None si erreur
        """
        try:
            # Télécharger le stream - retourne le chemin du fichier ou None
            downloaded_path = stream.download(
                output_path=str(output_dir), 
                filename=filename, 
                skip_existing=False
            )
            
            if not downloaded_path:
                logger.error(f"Flux {stream_type} non téléchargé (stream.download() retourna None)")
                return None
            
            # Callback final quand complète
            if progress_callback and stream.filesize > 0:
                progress_callback(stream.filesize, stream.filesize)
            
            logger.info(f"Flux {stream_type} téléchargé: {downloaded_path}")
            return downloaded_path
            
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement {stream_type}: {e}")
            return None
    
    def _merge_with_ffmpeg(
        self,
        video_path: str,
        audio_path: str,
        output_dir: Path,
        title: str,
        progress_callback: Optional[Callable] = None
    ) -> Optional[str]:
        """
        Fusionne vidéo et audio avec FFmpeg (multiplateforme via imageio-ffmpeg)
        
        Args:
            video_path: Chemin du fichier vidéo
            audio_path: Chemin du fichier audio
            output_dir: Répertoire de sortie
            title: Titre pour le nom du fichier final
            progress_callback: Callback pour tracker la progression de fusion (0-100%)
            
        Returns:
            Chemin du fichier fusionné ou None si erreur
        """
        output_file = output_dir / f"{title}.mp4"
        
        try:
            # Importer FFmpeg via imageio-ffmpeg (multiplateforme)
            try:
                import imageio_ffmpeg as ffmpeg
                ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
                logger.info(f"Utilisation de FFmpeg: {ffmpeg_exe}")
            except (ImportError, RuntimeError) as e:
                logger.error(f"Impossible de charger imageio-ffmpeg: {e}")
                return None
            
            # Construire la commande FFmpeg
            # -c copy : copier les codecs sans réencodage (ultra rapide)
            cmd = [
                ffmpeg_exe,
                "-i", video_path,        # Fichier vidéo d'entrée
                "-i", audio_path,        # Fichier audio d'entrée
                "-c:v", "copy",          # Copier le codec vidéo
                "-c:a", "aac",           # Codec audio (aac compatible)
                "-shortest",             # Limiter à la durée la plus courte
                str(output_file),        # Fichier de sortie
                "-y"                     # Écraser si existe
            ]
            
            # Déterminer les flags selon le système pour masquer la fenêtre
            creationflags = 0
            if Config.IS_WINDOWS:
                creationflags = subprocess.CREATE_NO_WINDOW
            
            # Exécuter FFmpeg
            logger.info("Fusion vidéo et audio avec FFmpeg...")
            
            # Simuler la progression de fusion tous les 200ms
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creationflags
            )
            
            # Tracker la progression pendant la fusion
            merge_start_time = time.time()
            progress_step = 0
            max_steps = 50  # 50 steps pour arriver à 100%
            
            while process.poll() is None:
                if progress_callback and progress_step < max_steps:
                    # Incrementer progressivement (0-100%)
                    merge_progress = (progress_step / max_steps) * 100
                    progress_callback(merge_progress)
                    progress_step += 1
                
                time.sleep(0.1)  # Mettre à jour tous les 100ms
            
            # Assurer que la progression atteint 100%
            if progress_callback:
                progress_callback(100)
            
            # Vérifier le résultat
            returncode = process.returncode
            if returncode == 0:
                logger.info(f"Fusion complétée: {output_file}")
                return str(output_file)
            else:
                _, stderr = process.communicate()
                logger.error(f"Erreur FFmpeg (code {returncode}): {stderr}")
                return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la fusion: {e}")
            return None
    
    def _download_subtitle(
        self,
        subtitle_code: str,
        output_dir: Path,
        title: str
    ) -> bool:
        """
        Télécharge les sous-titres
        
        Args:
            subtitle_code: Code de langue pour les sous-titres
            output_dir: Répertoire de sortie
            title: Titre vidéo pour le nom du fichier
            
        Returns:
            True si succès, False sinon
        """
        try:
            caption = self.handler.get_caption_by_code(subtitle_code)
            if not caption:
                logger.warning(f"Sous-titre non trouvé pour le code {subtitle_code}")
                return False
            
            subtitle_file = output_dir / f"{title}_{subtitle_code}.vtt"
            caption.save(str(subtitle_file))
            logger.info(f"Sous-titres téléchargés: {subtitle_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement des sous-titres: {e}")
            return False
    
    def _cleanup_temp_files(self):
        """Nettoie les fichiers temporaires après fusion"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.info(f"Fichier temporaire supprimé: {temp_file}")
            except Exception as e:
                logger.warning(f"Impossible de supprimer {temp_file}: {e}")
        
        # Réinitialiser la liste
        self.temp_files = []
    
    @staticmethod
    def _make_safe_filename(filename: str) -> str:
        """
        Crée un nom de fichier sûr pour tous les systèmes de fichiers
        
        Args:
            filename: Nom original
            
        Returns:
            Nom sûr sans caractères interdits
        """
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:200]  # Limiter la longueur
    
    def cancel_download(self):
        """Annule le téléchargement en cours"""
        self.is_downloading = False
        logger.info("Annulation du téléchargement demandée")

