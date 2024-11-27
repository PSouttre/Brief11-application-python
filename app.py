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
    df = df[df['intitule'].str.contains(input_intitule, case=False, na=False)]       # Filtrer les données en fonction de l'intitulé du poste sans tenir compte de la casse   
   
    if df.empty :
        st.error(f"Ce poste n'existe pas dans la base")
    else: 
        print("Entrée input poste valide") 
else: 
    print("Marque filtrée")

# Filtre par Titre de Poste 
titre_poste = st.sidebar.selectbox ( 
    'Sélectionner le titre de poste', 
    options=df['intitule'].unique(), 
    index = 0
) 
# Convertir titre_poste en liste
#titre_poste_list = [titre_poste] if titre_poste else []

#if titre_poste_list :
#   df = df[df['intitule'].isin(titre_poste_list)]

# Filtre par Localisation 
#localisation = st.sidebar.multiselect( 
#   'Sélectionner la localisation', 
#    options=df['lieuTravail_libelle'].unique(), 
#   default=df['lieuTravail_libelle'].unique() 
#) 

# Filtre par Entreprise 
#entreprise = st.sidebar.multiselect( 
#   'Sélectionner l\'entreprise', 
#    options=df['entreprise_nom'].unique(), 
 #   default=df['entreprise_nom'].unique() ) 

# Appliquer les filtres aux données 
#filtered_df = df[ (df['intitule'].isin(titre_poste_list)) 
                 #& (df['lieuTravail_libelle'].isin(localisation)) & (df['entreprise_nom'].isin(entreprise)) 
#                 ] 

# Afficher les données filtrées 
st.write('Données Filtrées', df)