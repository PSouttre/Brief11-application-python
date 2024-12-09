import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import requests
import matplotlib.pyplot as plt
from datetime import datetime

DB_URL = ("postgresql://PS:Password@localhost/PS" )
API_URL = "http://127.0.0.1:5000/api/data"

engine = create_engine(DB_URL)

st.title("Visualisation des Offres d'Emploi")

@st.cache_data
def fetch_data_from_db():
    query = 'SELECT * FROM "Job5";'  
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
#data = fetch_data_from_db()


df = data
st.write(df.shape)
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


# Filtre par Lieu de Travail
lieuTravail = st.sidebar.selectbox(
    'Sélectionner un lieu de travail',
    options=['Tous'] + sorted(list(final_df['departement'].unique())),
    key="selectbox_lieu"
)

# Appliquer le filtre Lieu de Travail si des options sont sélectionnées
if lieuTravail != 'Tous':
    final_df = final_df[final_df['departement'] == lieuTravail]

# Filtre par Type de Contrat
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


# Afficher les données filtrées 
st.write('Données Filtrées', final_df)

##########################################################################################################################
# Graphes
##########################################################################################################################


################################## Repartition des offres selon le type de contrat #########################################"


def pie_chart(final_df, lieuTravail):

    # Comptage des types de contrat
    contrat_counts = final_df['typeContrat'].value_counts()

    # Création de la figure avec une taille ajustée
    fig, ax = plt.subplots(figsize=(2, 2))

    # Graphique en camembert
    wedges, texts, autotexts = ax.pie(contrat_counts,               # texts (labels) et autotexts (%) permet de personnaliser les tailles de police et améliorer la lisibilité
                                      autopct='%1.1f%%',            # Affiche les % à l'intérieur des parts avec 1 seule décimale
                                      startangle=90, 
                                      colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], 
                                      pctdistance= 1.2,
                                      textprops={'size': 'smaller'})
    
    ax.axis('equal')  # Pour que le graphique soit circulaire

    # Taille de police
    for text in texts:
        text.set_fontsize(5)

    # Taille de police pour les pourcentages 
    for autotext in autotexts: 
        autotext.set_fontsize(3)
    
    # Mettre à jour le titre en fonction des filtres
    title = "Répartition des types de contrat"

    # Si un lieu de travail est sélectionné (autre que 'Tous')
    if lieuTravail != 'Tous':
        title += f" pour le département {lieuTravail}"


    # Définir le titre du graphique
    plt.title(title, fontsize = 5, pad = 20)
    

    # La légende associe chaque type de contrat à une couleur spécifique
    labels = contrat_counts.index.tolist()
    ax.legend(wedges, labels, title="Types de Contrat", loc="center left", bbox_to_anchor=(1, 0.5), fontsize= 5, title_fontsize = 5)

    # Affichage du graphique avec Streamlit
    st.pyplot(fig)


pie_chart(final_df, lieuTravail)


##################################   Parts selon le code ROME  #########################################

rome_counts = final_df['romeCode'].value_counts()

# Dictionnaire de correspondance entre romeCode et intitulé
rome_to_intitule = {
    'E1101' : 'Community Manager', 
    'E1104': 'Concepteur de contenus multimédia',
    'E1206': 'UX UI Designer', 
    'M1801': 'Admin Réseau', 
    'M1802': 'Ingénieur syst informatique ',
    'M1803':'DSI',
    'M1805': 'Dev Web',
    'M1806': 'Product Owner',
    'M1810': 'Technicien Informatique',
    'M1811': 'Data Ingineer',
    'M1812': 'RSSI',
    'M1813': 'Integrateurs logiciels métier'
}

# Remplacer les codes ROME par les intitulés correspondants
intitule_labels = [rome_to_intitule.get(code, code) for code in rome_counts.index]

# Création du graphique en barres
fig, ax = plt.subplots(figsize=(10, 6))  # Ajustez la taille du graphique si nécessaire

# Diagramme en barres
ax.bar(intitule_labels, rome_counts.values, color='#66b3ff')

# Ajout des labels et titre
ax.set_xlabel('Intitulé du poste selon code ROME', fontsize=12)
ax.set_ylabel('Nombre d\'offres', fontsize=12)
ax.set_title('Nombre d\'offres par Code ROME', fontsize=14)
#ax.tick_params(axis='x', rotation=45)  # Rotation des labels des abscisses pour éviter le chevauchement

# Rotation et alignement des labels des abscisses 
ax.set_xticklabels(intitule_labels, rotation=45, ha='right')

# Affichage du graphique
plt.tight_layout()  # Permet d'éviter le chevauchement des éléments
st.pyplot(fig)










