FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    --no-install-recommends && \
    apt-get clean 
   # rm -rf /var/lib/apt/lists/*

# Copier les fichiers de l'application
COPY . .

# Mettre à jour pip et installer les dépendances Python
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Ajouter ~/.local/bin au PATH
#ENV PATH="/root/.local/bin:$PATH"

# Commande par défaut pour lancer l'application
CMD ["streamlit", "run", " app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
#CMD ["sleep","infinity"]