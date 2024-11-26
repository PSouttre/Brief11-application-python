import streamlit as st
import requests

# URL de l'API Flask
api_url = 'http://localhost:5000/api/data'

st.title('Interface Streamlit')

# Requête à l'API Flask
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    st.write(f"Nom: {data.get('nom')}")
    st.write(f"Âge: {data.get('age')}")
else:
    st.write("Erreur lors de la récupération des données")
