import pandas as pd
import streamlit as st
import altair as alt
import pydeck as pdk
import requests
from datetime import datetime
import os

# Chemin vers le fichier CSV
FILE_PATH = "C:/Users/vahid/Documents/Brief11-application-python/Brief11-application-python/france_travail_nettoy\u00e9.csv"

# Fonction pour charger les données
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Le fichier {file_path} est introuvable.")
        return None
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            st.error("Le fichier de données est vide.")
            return None
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None

# Charger les données
data = load_data(FILE_PATH)

# Interface principale
st.title("Visualisation des données du marché de l'emploi")

if data is not None:
    # **1. Tableau des données**
    st.subheader("Tableau des données nettoyées")
    st.dataframe(data)

    # **2. Graphique des types de contrats**
    st.subheader("Répartition des types de contrats")
    type_contrat_chart = alt.Chart(data).mark_bar().encode(
        x='type_de_contrat',
        y='count()',
        color='type_de_contrat'
    ).properties(width=600, height=400)
    st.altair_chart(type_contrat_chart, use_container_width=True)

    # **3. Carte des lieux de travail**
    st.subheader("Carte des lieux de travail")
    if {'latitude', 'longitude', 'lieu_de_travail'}.issubset(data.columns):
        data_map = data[['latitude', 'longitude', 'lieu_de_travail']].dropna()
        map_layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_map,
            get_position='[longitude, latitude]',
            get_radius=1000,
            get_color=[200, 30, 0, 160],
            pickable=True,
        )
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=data_map['latitude'].mean(),
                longitude=data_map['longitude'].mean(),
                zoom=6,
                pitch=50,
            ),
            layers=[map_layer]
        ))
    else:
        st.warning("Les colonnes nécessaires pour la carte ne sont pas disponibles.")

    # **4. Filtres dynamiques dans la barre latérale**
    st.sidebar.title("Filtres de recherche")
    st.sidebar.markdown("---")

    selected_contract = st.sidebar.selectbox(
        "Type de contrat", options=data['type_de_contrat'].dropna().unique()
    )
    selected_location = st.sidebar.selectbox(
        "Lieu de travail", options=data['lieu_de_travail'].dropna().unique()
    )

    # Appliquer les filtres
    filtered_data = data[
        (data['type_de_contrat'] == selected_contract) &
        (data['lieu_de_travail'] == selected_location)
    ]

    # Afficher les données filtrées
    st.subheader(f"Données filtrées : {selected_contract}, {selected_location}")
    st.dataframe(filtered_data)

    # **5. Collecte des données depuis l'API**
    def collect_data(start_date, end_date=None):
        url = "http://127.0.0.1:5000/france-travail/collect"  # URL de l'API Flask
        data = {
            "start_date": start_date,  # Paramètre start_date
            "end_date": end_date       # Paramètre end_date (optionnel)
        }

        # On envoie une requête POST à l'API Flask avec les données en JSON
        response = requests.post(url, json=data)

        # Traitement de la réponse de l'API
        if response.status_code == 200:
            return response.json()  # Si la requête a réussi, on retourne les données
        else:
            return {"error": "Erreur lors de la collecte des données"}

    st.title("Collecte de données depuis France Travail")

    # Interface utilisateur pour saisir les dates
    start_date = st.date_input("Date de début")
    end_date = st.date_input("Date de fin (optionnel)", value=None)

    if st.button("Mettre à jour les données"):
        if start_date:
            # Envoie de la requête à l'API Flask avec les dates choisies
            data = collect_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d') if end_date else None)
            st.write(data)  # Affichage des résultats ou erreur
        else:
            st.error("La date de début est obligatoire")





