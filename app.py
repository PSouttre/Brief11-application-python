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

# Initialisation de final_df avec filtered_df
final_df = filtered_df    

# Filtre par Titre de Poste 
titre_poste = st.sidebar.selectbox ( 
    'Sélectionner le titre de poste', 
    options=['Tous'] + sorted(list(final_df['intitule'].unique())), 
    index = 0,
    key="selectbox_titre"
) 

# Appliquer un second filtre si un intitulé spécifique est sélectionné
if titre_poste != 'Tous':
    final_df = final_df[final_df['intitule'] == titre_poste]


# Filtrage par Lieu de Travail
lieuTravail = st.sidebar.selectbox(
    'Sélectionner un lieu de travail',
    options=['Tous'] + sorted(list(final_df['lieuTravail_libelle'].unique())),
    key="selectbox_lieu"
)

# Appliquer le filtre Lieu de Travail si des options sont sélectionnées
if lieuTravail != 'Tous':
    final_df = final_df[final_df['lieuTravail_libelle'] == lieuTravail]

# Filtrage par Type de Contrat
typeContrat = st.sidebar.selectbox(
    'Sélectionner un type de contrat',
    options=['Tous'] + sorted(list(final_df['typeContrat'].unique())),
      key = "selectbox_contrat"  # Ajouter l'option 'Tous'
)

# Appliquer le filtre Type de Contrat si des options sont sélectionnées
if typeContrat != 'Tous':
    final_df = final_df[final_df['typeContrat'] == typeContrat]

# Filtrage par Expérience
experienceLibelle = st.sidebar.selectbox(
    'Sélectionner un niveau d\'expérience',
    options=['Tous'] + sorted(list(final_df['experienceLibelle'].unique())),   # Ajouter l'option 'Tous'
    key = "selectbox_experience"  
)

# Appliquer le filtre Expérience si des options sont sélectionnées
if experienceLibelle != 'Tous':
    final_df = final_df[final_df['experienceLibelle'] == experienceLibelle]

# Mettre à jour la liste des intitulés dans le selectbox en fonction des données filtrées
titre_poste = st.sidebar.selectbox(
    'Sélectionner le titre de poste',
    options=['Tous'] + list(final_df['intitule'].unique()),
    key = "selectbox_poste"  # Ajouter 'Tous' pour voir tous les postes
)



# Afficher les données filtrées 
st.write('Données Filtrées', final_df)