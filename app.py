import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import requests

DB_URL = ("postgresql://Username:Password@localhost/Database_name" )
API_URL = "http://127.0.0.1:5000/api/data"

engine = create_engine(DB_URL)

st.title("Visualisation des Offres d'Emploi")

@st.cache_data
def fetch_data_from_db():
    query = 'SELECT * FROM "Job11";'  
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

data = fetch_data_from_db()

def update_data():
    try:
        response = requests.get(API_URL)  # Appel à l'API Flask
        if response.status_code == 200:
            st.success("Les données ont été mises à jour avec succès !")
        else:
            st.error(f"Erreur lors de la mise à jour des données : {response.status_code}")
    except Exception as e:
        st.error(f"Erreur lors de l'appel API : {e}")

if st.button("Mise à jour des données"):
    st.info("Mise à jour en cours...")
    update_data()  

st.subheader("Données récupérées depuis PostgreSQL")
data = fetch_data_from_db()

if not data.empty:
    st.write(data)  
    st.subheader("Statistiques rapides")
    st.write(data.describe())  #
else:
    st.warning("Aucune donnée disponible dans la base de données.")