FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt dans le répertoire de travail
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande pour lancer l'application
CMD ["python", "app_flask.py"]