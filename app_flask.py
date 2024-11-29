###########################################################
################# tout les imports standard ################
###########################################################
import re 
import os 
import datetime

###########################################################
################ modules externes #########################
###########################################################
import requests
import pandas as pd
from offres_emploi import Api
from flask import Flask, jsonify
from urllib.parse import quote_plus
from collections.abc import MutableMapping
from sqlalchemy.engine import create_engine
from offres_emploi.utils import dt_to_str_iso

app = Flask(__name__)

client = Api(client_id="yourid", 
             client_secret="yourapisecretpsswd")


engine = create_engine("postgresql://Username:Password@localhost/Database_name" )

@app.route('/api/data')
def get_data():
    start_dt = datetime.datetime(2019, 3, 1, 12, 30)
    end_dt = datetime.datetime.today()
    params = {
        "codeROME": ['M1802','M1805','M1810','M1815','M1820', 'M1825', 'M1830', 'M1835'],
        'minCreationDate': dt_to_str_iso(start_dt),
        'maxCreationDate': dt_to_str_iso(end_dt)
    }
    search_on_big_data = client.search(params=params)

    results =  search_on_big_data['resultats']

    def flatten(dictionary, parent_key='', separator='_'):
        items = []
        for key, value in dictionary.items():
            new_key = parent_key + separator + key if parent_key else key
            if isinstance(value, MutableMapping):
                items.extend(flatten(value, new_key, separator=separator).items())
            else:
                items.append((new_key, value))
        return dict(items)

    all_results_flatten = [flatten(result) for result in results]

    results_df = pd.DataFrame(all_results_flatten)

    new_df = results_df.drop(columns =  ['id','competences','qualitesProfessionnelles','lieuTravail_codePostal','lieuTravail_commune','typeContratLibelle','appellationlibelle','entreprise_nom','entreprise_entrepriseAdaptee', 'natureContrat', 'experienceExige','nombrePostes', 'accessibleTH','origineOffre_origine','origineOffre_partenaires','entreprise_description','dureeTravailLibelle','dureeTravailLibelleConverti','secteurActivite','secteurActiviteLibelle','salaire_libelle', 'salaire_commentaire','qualificationCode', 'qualificationLibelle','salaire_complement1', 'salaire_complement2','formations','contact_nom','contact_coordonnees1','contact_coordonnees2', 'contact_coordonnees3','agence_courriel','deplacementCode','deplacementLibelle', 'offresManqueCandidats','contact_courriel', 'experienceCommentaire','langues','contact_urlPostulation', 'complementExercice', 'origineOffre_urlOrigine'])

    new_df['dateCreation'] = pd.to_datetime(results_df['dateCreation'], errors='coerce') 
    new_df['dateActualisation'] = pd.to_datetime(results_df['dateActualisation'], errors='coerce')
    new_df['dateCreation'] = new_df['dateCreation'].dt.strftime("%Y-%m-%d") 
    new_df['dateActualisation'] = new_df['dateActualisation'].dt.strftime("%Y-%m-%d")
    new_df[['Département', 'Ville']] = new_df['lieuTravail_libelle'].str.split('-', expand=True, n=1)
    nouvel_ordre = ['intitule', 'description', 'dateCreation', 'dateActualisation','lieuTravail_libelle', 'Département', 'Ville', 'lieuTravail_latitude', 'lieuTravail_longitude','romeCode', 'romeLibelle', 'typeContrat', 'experienceLibelle','alternance', 'codeNAF']
    new_df = new_df[nouvel_ordre]
    if_exists = 'replace'

    with engine.connect() as con:
        new_df.to_sql(
        name="Job11", 
        con=con ,
        if_exists=if_exists
        )
    
    return 'Chaine de charactere'
if __name__ == '__main__':
    app.run(debug=True)