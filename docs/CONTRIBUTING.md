# Guide de Contribution à Yuload

Merci d'être intéressé par la contribution à Yuload ! Ce document explique l'architecture du projet, comment il fonctionne et comment vous pouvez contribuer.

**Créateur:** Josué Luis  
**Organisation:** Walborn

## Architecture du projet

Yuload suit une architecture modulaire et scalable, divisée en trois domaines principaux :

### Structure des répertoires

```
yuload/
├── core/                      Logique métier
│   ├── youtube_handler.py    Interactions avec l'API YouTube
│   └── downloader.py         Gestion des téléchargements
├── ui/                        Interface utilisateur
│   ├── main_window.py        Fenêtre principale de l'application
│   ├── widgets.py            Composants personnalisés Tkinter
│   └── styles.py             Thème et style
└── utils/                     Utilitaires
    ├── config.py             Gestion de la configuration
    ├── logger.py             Configuration du logging
    ├── http.py               Client HTTP avec httpx
    └── validators.py         Validation des entrées
```

### Modules principaux

#### YouTubeHandler (`yuload/core/youtube_handler.py`)

Gère toutes les interactions avec YouTube :
- Récupération des informations vidéo
- Vérification de disponibilité des flux
- Gestion des sous-titres et des légendes

#### Downloader (`yuload/core/downloader.py`)

Orchestre le processus de téléchargement :
- Téléchargement en threads multiples
- Suivi en temps réel de la progression
- Fusion vidéo/audio avec FFmpeg
- Téléchargement des sous-titres
- Nettoyage automatique des fichiers temporaires

#### MainWindow (`yuload/ui/main_window.py`)

Interface professionnelle incluant :
- Saisie et validation d'URL
- Affichage des métadonnées vidéo
- Sélecteur de qualité avec tailles de fichier
- Sélecteur de sous-titres
- Barre de progression animée
- Messages de statut en temps réel

#### LoadingSpinner (`yuload/ui/widgets.py`)

Widget personnalisé de chargement :
- Animation GIF fluide pendant le téléchargement
- Coche verte animée à la fin
- Fallback sur une animation dessinée si le GIF n'est pas disponible

### Configuration (`yuload/utils/config.py`)

Gestion centralisée de la configuration :
- Répertoires de base (downloads, logs, temporaires)
- Détection de plateforme (Windows, Linux, macOS)
- Configuration FFmpeg
- Paramètres de l'interface

## Flux de téléchargement

### Phases de téléchargement

1. Validation de l'URL YouTube
2. Récupération des informations vidéo (titre, durée, streams)
3. Sélection par l'utilisateur (qualité, sous-titres)
4. Phase 1 (0-33%) : Téléchargement du flux vidéo
5. Phase 2 (33-66%) : Téléchargement du flux audio
6. Phase 3 (66-100%) : Fusion avec FFmpeg
7. Nettoyage des fichiers temporaires

### Threading et sécurité

L'application utilise :
- Threads séparés pour les téléchargements (évite les blocages UI)
- `self.after()` pour tous les appels UI (thread-safety Tkinter)
- Callbacks pytubefix pour le suivi en temps réel des bytes
- Gestion automatique des ressources

## Prérequis

Pour contribuer au projet, installez :

- Python 3.9 ou supérieur (requis par pytubefix)
- Tkinter (inclus généralement avec Python)
- FFmpeg (pour la fusion audio/vidéo)

## Dépendances du projet

Principales dépendances :

- **pytubefix** (v10.3.8+) : API YouTube avec callbacks de progression
- **httpx** (v0.25.0+) : Client HTTP asynchrone
- **Pillow** (v10.0.0+) : Traitement d'images et GIF
- **imageio-ffmpeg** : Bundled FFmpeg pour fusionner les fichiers

## Structure des composants

### Cycle de vie d'une application

```
1. main.py -> Crée MainWindow
2. MainWindow.__init__() -> Initialise tous les widgets
3. Utilisateur colle URL -> _load_video_thread() lance dans un thread
4. YouTubeHandler récupère les infos
5. Utilisateur sélectionne qualité + sous-titres
6. Utilisateur clique "Télécharger" -> Downloader.download_video()
7. Downloader.__init__() enregistre les callbacks Tkinter
8. _download_video_thread() orchestre la progression
9. Callbacks mettent à jour la barre de progression via self.after()
10. Fichier sauvegardé, spinner affiche coche verte
```

### Intégration des callbacks

Les callbacks sont enregistrés dans MainWindow et passés au Downloader :

```python
downloader = Downloader(
    youtube_handler,
    on_progress=safe_progress_callback,
    on_status_update=safe_status_callback,
    on_completion=safe_completion_callback,
    on_error=safe_error_callback
)
```

Tous les callbacks sont wrappés avec `self.after()` pour assurer la thread-safety.

## Installation pour le développement

### 1. Cloner le projet
```bash
cd /path/to/yuload
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
python main.py
```

## Code structure et bonnes pratiques

### Conventions de nommage

- Classes : PascalCase (ex: `YouTubeHandler`, `LoadingSpinner`)
- Fonctions/méthodes : snake_case (ex: `download_video()`, `on_progress()`)
- Constantes : UPPER_CASE (ex: `DEFAULT_TIMEOUT`, `CHUNK_SIZE`)
- Variables privées : prefix underscore (ex: `_client`, `_current_phase`)

### Documentation du code

- Tous les commentaires et docstrings en français
- Type hints complets pour meilleure IDE support
- Documentation des edge cases et des dépendances

Exemple :

```python
def download_video(self, url: str, quality: str, callback: Callable) -> None:
    """
    Télécharger une vidéo YouTube avec fusion audio/vidéo.
    
    Args:
        url: Adresse YouTube validée
        quality: Qualité au format '720p', '1080p', etc.
        callback: Fonction appelée lors de chaque mise à jour
    
    Raises:
        ValueError: Si l'URL ou la qualité est invalide
    """
```

### Gestion des erreurs

- Try/catch avec logging détaillé
- Messages d'erreur clairs pour l'utilisateur
- Fallbacks gracieux (ex: spinner dessiné si GIF échoue)
- Cleanup automatique des ressources

### Tests

Bien que le projet actuel utilise des tests d'intégration simples, pour contribution future :

- Tests unitaires pour chaque module
- Tests d'intégration pour les workflows complets
- Fixtures pour les datas YouTube mockées
- Coverage > 80%

## Extension de l'application

### Ajouter des filtres de qualité

Dans `YouTubeHandler._get_available_qualities()` :

```python
# Filtrer par codec, fps, résolution
valid_streams = [s for s in streams if s.resolution]
```

### Créer de nouveaux widgets UI

Étendre `tk.Canvas` ou `tk.Frame` dans `widgets.py` :

```python
class NewWidget(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Initialiser le widget
```

### Ajouter des options de configuration

Ajouter dans `config.py` :

```python
NEW_SETTING = getenv('YULOAD_NEW_SETTING', 'default_value')
```

## Commandes utiles

```bash
# Vérifier la syntaxe
python3 -m py_compile yuload/**/*.py

# Exécuter les tests
python test_integration.py

# Lancer en mode débogage
python -u main.py

# Avec uv
uv run python main.py
```

## Dépannage en développement

### Import errors
Assurez-vous que l'environnement virtuel est activé et les dépendances sont installées.

### Erreurs Tkinter
Vérifiez que Tkinter est installé : `python -m tkinter`

### Erreurs FFmpeg
Vérifiez que FFmpeg est dans le PATH : `which ffmpeg` ou `where ffmpeg` (Windows)

### Problèmes de threading
Si UI se gèle, vérifiez que tous les appels UI utilisent `self.after()`

## Principes de design

- Modularité : Chaque composant responsable d'une tâche unique
- Extensibilité : Code structuré pour être facile à étendre
- Thread-safety : Toutes les opérations thread-safe par défaut
- User-centric : Messages clairs et interface intuitive
- Robustesse : Fallbacks pour tous les cas d'erreur

## Historique des changements

Consultez [CHANGELOG.md](CHANGELOG.md) pour l'historique complet des changements.

## Rapport de bugs

Si vous trouvez un bug :
1. Vérifiez les fichiers de log dans ~/.yuload/logs/
2. Décrivez les étapes pour reproduire
3. Incluez votre version de Python et de l'OS
4. Attachez les logs pertinents

## Suggestion de fonctionnalités

Les suggestions sont bienvenues ! Pensez à :
- Historique de téléchargements
- Pause/reprise des téléchargements
- Support des playlists
- Thèmes personnalisés supplémentaires
- Conversion de formats

## Licence

Ce projet est fourni à titre gratuit pour usage personnel.

---

Merci de votre contribution à Yuload !
