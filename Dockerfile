# Étape 1 : Utiliser une image Python de base
FROM python:3.10-slim

# Étape 2 : Mettre à jour le gestionnaire de paquets et installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Étape 3 : Définir le répertoire de travail
WORKDIR /app

# Étape 4 : Copier les fichiers nécessaires dans l'image Docker
COPY . .

# Étape 5 : Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6 : Exposer les ports nécessaires
EXPOSE 5000 8501

# Étape 7 : Commande par défaut
CMD ["bash", "-c", "python app_flask.py & streamlit run app.py"]
