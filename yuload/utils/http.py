"""Utilitaires HTTP utilisant httpx pour les requêtes API"""

import httpx
from typing import Optional, Dict, Any
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class HTTPClient:
    """Client HTTP utilisant httpx pour les requêtes GET/POST"""
    
    # Délai d'expiration par défaut (10 secondes)
    DEFAULT_TIMEOUT = 10.0
    # En-têtes HTTP par défaut pour les requêtes
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        """
        Initialise le client HTTP.
        
        Args:
            timeout: Délai d'expiration des requêtes en secondes
        """
        self.timeout = timeout
        # Client httpx créé à la demande (lazy initialization)
        self._client: Optional[httpx.Client] = None
    
    @property
    def client(self) -> httpx.Client:
        """
        Récupère ou crée le client httpx.
        Utilise le pattern lazy initialization pour économiser les ressources.
        
        Returns:
            Client httpx configuré
        """
        if self._client is None:
            self._client = httpx.Client(
                timeout=self.timeout,
                headers=self.DEFAULT_HEADERS
            )
        return self._client
    
    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[httpx.Response]:
        """
        Effectue une requête HTTP GET.
        Gère automatiquement les erreurs et le logging.
        
        Args:
            url: URL cible
            params: Paramètres de requête optionnels
            headers: En-têtes HTTP additionnels optionnels
            
        Returns:
            Objet Response ou None en cas d'erreur
        """
        try:
            # Fusion des en-têtes (headers additionnels + defaults)
            merged_headers = {**self.DEFAULT_HEADERS, **(headers or {})}
            
            response = self.client.get(
                url,
                params=params,
                headers=merged_headers
            )
            # Lève une exception si le code HTTP indique une erreur
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            # Erreurs de connexion, timeout, etc.
            logger.error(f"Erreur de requête HTTP: {e}")
            return None
        except Exception as e:
            # Erreurs inattendues
            logger.error(f"Erreur inattendue lors de la requête GET: {e}")
            return None
    
    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[httpx.Response]:
        """
        Effectue une requête HTTP POST.
        Supporte les données form et JSON.
        
        Args:
            url: URL cible
            data: Données de formulaire optionnelles
            json: Corps JSON optionnel
            headers: En-têtes HTTP additionnels optionnels
            
        Returns:
            Objet Response ou None en cas d'erreur
        """
        try:
            merged_headers = {**self.DEFAULT_HEADERS, **(headers or {})}
            
            response = self.client.post(
                url,
                data=data,
                json=json,
                headers=merged_headers
            )
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            logger.error(f"Erreur de requête HTTP: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la requête POST: {e}")
            return None
    
    def close(self):
        """
        Ferme le client HTTP et libère les ressources.
        Important : appeler cette méthode avant de quitter l'application.
        """
        if self._client:
            self._client.close()
            self._client = None
    
    def __enter__(self):
        """Support du context manager (with statement)"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme automatiquement le client à la sortie du context manager"""
        self.close()


# Instance globale du client HTTP (singleton)
_http_client: Optional[HTTPClient] = None


def get_http_client() -> HTTPClient:
    """
    Récupère l'instance globale du client HTTP (singleton pattern).
    Assure qu'un seul client HTTP est utilisé dans toute l'application.
    
    Returns:
        Instance globale du HTTPClient
    """
    global _http_client
    if _http_client is None:
        _http_client = HTTPClient()
    return _http_client
