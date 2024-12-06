import os 
import json
import requests
import pandas as pd 
from pprint import pprint
from dotenv import load_dotenv
from openai import AzureOpenAI
from sqlalchemy import create_engine

###########################################################################################################################################
#                                Initialisation du client et chargement des données depuis la BDD PostgreSQL
###########################################################################################################################################

DB_URL = ("postgresql://Yildirim:Yildirim31@localhost/Yildirim" )
engine = create_engine(DB_URL)

print(load_dotenv())

AZUR_ENDPOINT = os.getenv("AZUR_ENDPOINT")
AZUR_KEY = os.getenv("AZUR_KEY")

query = 'SELECT * FROM "Job3";'  
with engine.connect() as connection:
    df = pd.read_sql(query, connection)


## Initialisation du client Azure OpenAI
client = AzureOpenAI(
    api_key=AZUR_KEY,  
    api_version="2024-10-21",
    azure_endpoint=AZUR_ENDPOINT
    )

## Modèle de langage spécifié sur Azure
#deployment_name="gpt-35-turbo"

## Récupération de la colonne 'description' de la 1ère offre
#job_description = df.loc[0, "description"]

#print(job_description)


###########################################################################################################################################
#                                Extraction des compétences
###########################################################################################################################################


# Fonction pour extraire les données

def extract_skills(job_description):
    prompt =\
    """
    Ta tâche est d'extraire des compétences mentionnées dans une offres d'emploi. Ton objectif est d'extraire et de catégoriser ces compétences sous format json.
    Extrait les compétences selon le schéma suivant: {category1: [compétence1, compétence2, etc.], category2: [compétence3, compétence4, etc.]}. 
    Assume everything mentioned refers to the same thing. 
    The extracted information should be categorized according to the allowed categories specified below.

    Constraints:
    - Allowed Categories: "Hard skill", "Soft skill", "Technologie"
    
    """
    prompt += f"Input: {job_description}"
    prompt += "\nOutput:"

        

# Nom du déploiement du modèle 
    deployment_name="gpt-4-turbo-2024-04-09"

# Création d'une complétion du chat
    completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    response = completion.choices[0].message.content
    data = json.loads(response)

    return data.get("Hard skill", []), data.get("Soft skill", []), data.get("Technologie", [])
