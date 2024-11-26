import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.title("Offres d'emploi")

# Récupération des données depuis un fichier csv
df = pd.read_csv("./df_tech_clean.csv", delimiter = ',', encoding='utf-8')


##########################################################################################################################
# Implémenter la fonctionnalité de tri du jeu de données
##########################################################################################################################



# Filtre par Titre de Poste 
titre_poste = st.sidebar.multiselect( 'Sélectionner le titre de poste', options=df['intitule'].unique(), default=df['intitule'].unique() ) 

# Filtre par Localisation 
localisation = st.sidebar.multiselect( 'Sélectionner la localisation', options=df['lieuTravail_libelle'].unique(), default=df['lieuTravail_libelle'].unique() ) 

# Filtre par Entreprise 
entreprise = st.sidebar.multiselect( 'Sélectionner l\'entreprise', options=df['entreprise_nom'].unique(), default=df['entreprise_nom'].unique() ) 

# Appliquer les filtres aux données 
filtered_df = df[ (df['intitule'].isin(titre_poste)) & (df['lieuTravail_libelle'].isin(localisation)) & (df['entreprise_nom'].isin(entreprise)) ] 

# Afficher les données filtrées 
st.write('Données Filtrées', filtered_df)