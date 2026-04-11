FROM ubuntu:20.04

# Prérequis système et locales
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    software-properties-common wget curl xz-utils git patchelf binutils \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev \
    libssl-dev ca-certificates python3-tk \
    && add-apt-repository ppa:deadsnakes/ppa -y


# Installation de Python 3.10 et Tkinter
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-tk

# Téléchargement de FFmpeg Statique (John Van Sickle)
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ -C /tmp && \
    mv /tmp/ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/ffmpeg && \
    mv /tmp/ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ffprobe && \
    rm -rf /tmp/ffmpeg-*

# Installation de 'uv'
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Environnement Python et dépendances
RUN uv venv .venv --python 3.10
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml . 
RUN uv pip install . pyinstaller

# Copie du code source
COPY . .

# Téléchargement de appimagetool
RUN wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O /usr/local/bin/appimagetool && \
    chmod +x /usr/local/bin/appimagetool

# Script de build final
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
