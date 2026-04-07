# Migration vers httpx et uv

## Changements effectués

### 1. Remplacement de `requests` par `httpx`

- **Fichiers modifiés:**
  - `pyproject.toml` - Remplacé `requests>=2.31.0` par `httpx>=0.25.0`
  - `requirements.txt` - Remplacé `requests==2.31.0` par `httpx==0.25.0`

- **Nouveaux fichiers:**
  - `yuload/utils/http.py` - Module HTTP client utilisant httpx
    - `HTTPClient` classe pour les requêtes HTTP
    - `get_http_client()` pour obtenir l'instance globale
    - Support complet des requêtes GET et POST

### 2. Configuration pour uv

- **pyproject.toml** - Configuration déjà présente pour uv
  - Gestion des dépendances via uv
  - Support de Python 3.9+

### 3. Utilisation

#### Synchroniser les dépendances:
```bash
uv sync
```

#### Lancer l'application:
```bash
uv run python3 main.py
```

#### Ou avec l'environnement virtuel:
```bash
source .venv/bin/activate
python3 main.py
```

### 4. Avantages de httpx

- API asynchrone (async/await support)
- Plus rapide que requests
- Meilleur support pour HTTP/2
- Type hints complets
- Meilleure gestion des ressources

### 5. Avantages de uv

- Gestionnaire de dépendances ultra-rapide
- Résolution de dépendances déterministe
- Gestion automatique des versions Python
- Lock file reproductible avec `uv.lock`

## Migration complète

Tous les modules Yuload sont maintenant configurés pour:
- Utiliser `httpx` pour les requêtes HTTP
- Être gérés par `uv` pour les dépendances
- Maintenir la compatibilité avec pip/virtualenv

L'application fonctionne exactement de la même manière, mais avec des dépendances plus modernes et performantes.
