import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.title("Offres d'emploi")

# Récupération des données depuis un fichier csv
df = pd.read_csv("./df_tech_clean3.csv", delimiter = ',', encoding='utf-8')


##########################################################################################################################
# Implémenter la fonctionnalité de tri du jeu de données
##########################################################################################################################


# Création du input pour le poste
input_intitule = st.sidebar.text_input ('Intitulé du poste')
if input_intitule :
    filtered_df = df[df['intitule'].str.contains(input_intitule, case=False, na=False)]       # Filtrer les données en fonction de l'intitulé du poste sans tenir compte de la casse   
   
    if filtered_df.empty :
        st.error(f"Ce poste n'existe pas dans la base")
    else: 
        print("Entrée input poste valide") 
else: 
    filtered_df = df

# Filtre par Titre de Poste 
titre_poste = st.sidebar.selectbox ( 
    'Sélectionner le titre de poste', 
    options=['Tous'] + list(filtered_df['intitule'].unique()), 
    index = 0
) 
# Appliquer un second filtre si un intitulé spécifique est sélectionné
if titre_poste != 'Tous':
    final_df = filtered_df[filtered_df['intitule'] == titre_poste]
else:
    final_df = filtered_df  # Si 'Tous' est sélectionné, afficher tous les postes filtrés


# Afficher les données filtrées 
st.write('Données Filtrées', final_df)