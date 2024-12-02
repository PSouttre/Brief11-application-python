Coder une application d'analyse du marché du travail de la tech

L'objectif est de développer une application de collecte, stockage et visualisation de données relatives au marché de l'emploi de la tech en France.
Les données relatives aux offres d'emplois sont collectées depuis l'API de France Travail.
Les données collectées doivent être automatiquement nettoyées et stockées dans une base de données.
Une interface doit permettre de visualiser les données.
Rédiger une analyse du marché du travail de la tech en France



Principales problématiques techniques :

- Sélectionner les lignes et les colonnes pertinentes
- Nettoyer le jeu de données
- Coder l'interface web de visualisation (table et graphs). La visualisation doit être pertinente au regard de l'objectif poursuivi
- Utiliser un modèle génératif de texte pour extraire les information (notamment les compétences) des descriptions des offres d'emploi
- Créer une base de données (PostgreSQL)
- Alimenter la base de données
- Modifier l'application Streamlit pour qu'elle récupère les données depuis la base de données et non depuis le fichier CSV
- Coder un script de collecte automatique des nouvelles données depuis l'API France travail
- "Empaqueter" le script de collecte des données dans une API (par exemple avec Flask)
- Dans l'API, créer un endpoint "/france-travail/collect" qui reçoit deux paramètres : date de début de la collecte (requis) et date de fin de la collecte (optionnel)
- Coder un bouton pour exécuter la mise à jour des données depuis l'interface web
- Coder un pipeline de nettoyage et de stockage automatique des données dans l'API
- Toute l'application doit fonctionner avec Docker et Docker compose
