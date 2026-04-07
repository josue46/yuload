# Yuload - Téléchargeur YouTube

Télécharger vos vidéos YouTube préférées en haute qualité, avec audio parfaitement synchronisé.

Créateur: Josué Luis Martin Panzu
Organisation: Walborn

## Qu'est-ce que Yuload ?

Yuload est une application simple et intuitive qui vous permet de télécharger des vidéos YouTube en quelques clics. Contrairement aux autres téléchargeurs, Yuload télécharge automatiquement la vidéo ET l'audio séparément, puis les fusionne pour obtenir un fichier MP4 complet avec le son intégré.

## Installation

### Prérequis

- Python 3.9 ou supérieur
- Tkinter (inclus avec Python)
- FFmpeg (pour la fusion audio/vidéo - optionnel mais recommandé)

### Étape 1 : Télécharger le projet

```bash
cd /home/luis/Projects/yuload
```

### Étape 2 : Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Ou avec uv (plus rapide) :

```bash
uv sync
```

### Étape 4 : Installer FFmpeg (recommandé)

Ubuntu/Debian :
```bash
sudo apt-get install ffmpeg
```

macOS :
```bash
brew install ffmpeg
```

Windows :
Téléchargez depuis ffmpeg.org et ajoutez le chemin à votre PATH

## Utilisation

### Lancer l'application

```bash
python main.py
```

Ou avec uv :

```bash
uv run python main.py
```

### Comment télécharger une vidéo

1. Coller l'URL - Copiez l'adresse d'une vidéo YouTube et collez-la dans le champ URL
2. Charger - Cliquez sur le bouton "Charger la vidéo"
3. Attendre - Un spinner animé vous indique que l'application récupère les informations
4. Sélectionner la qualité - Choisissez la résolution de votre vidéo (1080p, 720p, 480p, etc.)
5. Ajouter des sous-titres - Si vous le souhaitez, sélectionnez la langue des sous-titres
6. Télécharger - Cliquez sur "Télécharger la vidéo" et choisissez le dossier de destination
7. Patienter - Observez la barre de progression pendant le téléchargement

### Où sont mes vidéos ?

Par défaut, les vidéos téléchargées sont sauvegardées dans le dossier :

```
~/.yuload/downloads
```

Vous pouvez cliquer sur "Ouvrir le dossier" pour accéder directement à vos téléchargements.

## Fonctionnalités principales

- Téléchargement d'URL YouTube - Copiez-collez simplement l'URL
- Multiples qualités - Choisissez votre résolution préférée
- Fusion audio automatique - Chaque vidéo inclut le son, fusionné dynamiquement
- Sous-titres - Télécharger les sous-titres en plusieurs langues
- Barre de progression animée - Suivez l'avancement du téléchargement en temps réel
- Interface moderne - Design sombre et professionnel
- Fenêtre d'accès rapide - Accédez directement à vos fichiers depuis l'application

## Résolution des problèmes

### "URL YouTube invalide"

Assurez-vous que :
- L'URL commence par youtube.com ou youtu.be
- L'URL est complète et valide
- La vidéo n'est pas supprimée ou rendue privée

### "Aucun flux disponible"

Cela signifie que la vidéo n'était pas disponible pour le téléchargement. Essayez :
- Vérifier votre connexion Internet
- Tenter avec une autre vidéo
- Vérifier votre VPN ou proxy

### "La barre de progression ne s'anime pas"

C'est normal pour les fichiers volumineux. L'application est en arrière-plan et se met à jour par portions de 1 MB. Le téléchargement est toujours en cours.

### "Le téléchargement résulte en vidéo sans son"

Cela signifie que FFmpeg n'est pas installé. Installez FFmpeg pour que Yuload fusionne correctement audio et vidéo.

## Logs et diagnostics

Si vous rencontrez des problèmes, les fichiers de log se trouvent ici :

```
~/.yuload/logs/
```

Ces fichiers contiennent des informations détaillées qui peuvent aider à diagnostiquer les problèmes.

## Conseils d'utilisation

- Qualité optimale : Choisissez 1080p ou 720p pour le meilleur rapport qualité/taille
- Téléchargement rapide : Les vidéos plus courtes se téléchargent plus vite
- Espace disque : Assurez-vous d'avoir suffisamment d'espace libre pour vos téléchargements
- Restriction de droits d'auteur : Téléchargez uniquement les vidéos pour lesquelles vous avez le droit de le faire

## Soutien

Si vous avez des questions ou rencontrez des problèmes :

1. Consultez la section "Résolution des problèmes"
2. Vérifiez les fichiers de log dans ~/.yuload/logs/
3. Assurez-vous que FFmpeg est correctement installé
4. Vérifiez votre connexion Internet

## Documentation pour les contributeurs

Pour les informations sur l'architecture, les fonctionnalités, le développement et comment contribuer au projet, consultez le fichier CONTRIBUTING.md dans le dossier docs/.

## Licence

Ce projet est fourni à titre gratuit pour usage personnel.

## Avertissement

Yuload est destiné au téléchargement de vidéos pour lesquelles vous avez l'autorisation. Respectez les lois sur le droit d'auteur et les conditions d'utilisation de YouTube. Les auteurs ne sont pas responsables de l'utilisation abusive de cet outil.

---

Profitez de Yuload et de vos téléchargements vidéo !