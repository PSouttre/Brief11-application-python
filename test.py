###########################################################
################# tous les imports standard ################
###########################################################
import re 
import os 
import datetime
import time
from datetime import timedelta, datetime
from copy import copy

###########################################################
################ modules externes #########################
###########################################################
import requests
import pandas as pd
from offres_emploi import Api
from flask import Flask, jsonify, request
from urllib.parse import quote_plus
from collections.abc import MutableMapping
from sqlalchemy.engine import create_engine
from offres_emploi.utils import dt_to_str_iso

app = Flask(__name__)

# authentification au pres de l'api
client = Api(client_id="PAR_buyan_50b2dfd1662001744a6862c407d2572ac60285a53c8fe625b20bace200321ee8", 
             client_secret="14b3b03b2508e7fe3c2e2ee446e48984d8a340b9758f0f9241de32817f43594e")

#connexion a la base SQL
engine = create_engine("postgresql://PS:Password@localhost/PS")

# applatir les données reçues : 
def flatten(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def collect_data(start, end, delta, code_rome):
    """
    Collecte récursive des données avec gestion de pagination et surcharge.
    """
    all_results = []
    local_start = copy(start)
    while local_start < end:
        time.sleep(2)
        local_end = local_start + delta
        print(f"Start getting data from {local_start} to {local_end}")
        results = []
        params = {
            "codeROME": code_rome,
            'minCreationDate': dt_to_str_iso(local_start),
            'maxCreationDate': dt_to_str_iso(local_end)
        }
        try:
            response = client.search(params=params)
            num_results = int(response.get("Content-Range", {}).get("max_results", 0))
            results = response.get("resultats", [])
        except AttributeError:
            print("No results. Continue...")
            num_results = 0
        except Exception as e:
            print("Error !!!!!!!!!!!!!!!!")
            print(e)
            print(type(e))
            num_results = 0

        if num_results > 149:
            print(f"Too much results: {num_results}")
            all_results += collect_data(local_start, local_end, delta / 2, code_rome)
        else:
            print(f"{num_results} results collected.")
            all_results += results

        local_start += delta

    return all_results


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"



@app.route('/api/data', methods=["GET"])
def get_data():
    # Récupérer les paramètres de la requête
    code_rome_param = request.args.get("codeROME", "M1802,M1805,E1101,E1104,E1206,M1801,M1806,M1810,M1811,M1812,M1813")  # Valeur par défaut
    start_dt = request.args.get("start_dt", "2024-08-01T12:30:00")
    end_dt = request.args.get("end_dt", datetime.today().isoformat())

    # Conversion de la chaîne de codes ROME en liste
    code_romes = code_rome_param.split(",")

    # Vérifier la validité des dates
    try:
        start_dt = datetime.fromisoformat(start_dt)
        end_dt = datetime.fromisoformat(end_dt)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format for start_dt or end_dt'}), 400

    # Durée des fenêtres d'interrogation
    delta = timedelta(days=3)

    # Collecter les données pour chaque code ROME
    all_results = []
    for code_rome in code_romes:
        print(f"Processing code ROME: {code_rome}")
        results = collect_data(start_dt, end_dt, delta, code_rome)
        all_results.extend(results)  # Ajouter les résultats collectés

    # Convertir et sauvegarder les résultats
    all_results_flatten = [flatten(result) for result in all_results]
    results_df = pd.DataFrame(all_results_flatten)

    # Suppression des colonnes inutiles
    new_df = results_df.drop(columns = ['id','lieuTravail_codePostal','lieuTravail_commune','typeContratLibelle','appellationlibelle','entreprise_nom',
    'entreprise_entrepriseAdaptee', 'natureContrat', 'experienceExige','nombrePostes', 'accessibleTH','origineOffre_origine',
    'origineOffre_partenaires','entreprise_description','dureeTravailLibelle','dureeTravailLibelleConverti','secteurActivite',
    'secteurActiviteLibelle','salaire_libelle', 'salaire_commentaire','qualificationCode', 'qualificationLibelle','salaire_complement1', 
    'salaire_complement2','formations','contact_nom','contact_coordonnees1','contact_coordonnees2', 'contact_coordonnees3','agence_courriel',
    'deplacementCode','deplacementLibelle', 'offresManqueCandidats','contact_courriel',  'experienceCommentaire','langues',
    'contact_urlPostulation',  'complementExercice', 'origineOffre_urlOrigine', 'qualitesProfessionnelles'])
    
    new_df['dateCreation'] = pd.to_datetime(results_df['dateCreation'], errors='coerce') 
    new_df['dateActualisation'] = pd.to_datetime(results_df['dateActualisation'], errors='coerce')
    new_df['dateCreation'] = new_df['dateCreation'].dt.strftime("%Y-%m-%d") 
    new_df['dateActualisation'] = new_df['dateActualisation'].dt.strftime("%Y-%m-%d")
    new_df[['departement', 'Ville']] = new_df['lieuTravail_libelle'].str.split('-', expand=True, n=1)
    nouvel_ordre = ['intitule', 'description', 'dateCreation', 'dateActualisation','lieuTravail_libelle', 'departement', 'Ville', 'lieuTravail_latitude', 'lieuTravail_longitude','romeCode', 'romeLibelle', 'typeContrat', 'experienceLibelle','alternance', 'codeNAF']
    new_df = new_df[nouvel_ordre]

    # Sauvegarde dans la base
    if_exists = 'replace'

    with engine.connect() as con:
        new_df.to_sql(
            name="Job5", index = False,
            con=con,
            if_exists=if_exists
        )

    return jsonify({'status': 'success', 'message': 'Data collected and stored successfully'}), 200





if __name__ == '__main__':
    app.run(debug=True)