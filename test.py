import requests
from offres_emploi import Api
import datetime
import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from sqlalchemy.engine import URL
from collections.abc import MutableMapping
import psycopg2
from offres_emploi.utils import dt_to_str_iso
import re 

client = Api(client_id="PAR_buyan_50b2dfd1662001744a6862c407d2572ac60285a53c8fe625b20bace200321ee8", 
             client_secret="14b3b03b2508e7fe3c2e2ee446e48984d8a340b9758f0f9241de32817f43594e")

from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
engine = create_engine("postgresql://Yildirim:Yildirim31@localhost/yil" )

#url = URL.create(
 #   drivername="postgresql",
  #  username="Yildirim",
   # host="postgres_container",
    #database="yil",
    #password="Yildirim31"
#)

#engine = create_engine(url)

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

#clean_col_names = lambda name: re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

#results_df.columns = [clean_col_names(c) for c in results_df.columns]

#results_df.rename(columns={"appellationlibelle": "appellation_libelle"}, inplace=True)
#results_df.rename(columns={"code_n_a_f": "code_naf"}, inplace=True)



new_df = results_df.drop(columns = ['id','qualitesProfessionnelles','dateCreation','dateActualisation','lieuTravail_latitude','competences', 'lieuTravail_longitude', 'lieuTravail_commune','typeContratLibelle','romeLibelle','appellationlibelle','entreprise_entrepriseAdaptee','typeContratLibelle','lieuTravail_latitude', 'lieuTravail_longitude', 'natureContrat', 'experienceExige','nombrePostes', 'accessibleTH','origineOffre_origine','origineOffre_partenaires','entreprise_description','dureeTravailLibelleConverti','codeNAF','secteurActivite', 'salaire_commentaire','qualificationCode', 'qualificationLibelle','salaire_complement1', 'salaire_complement2','formations','contact_nom','deplacementCode','deplacementLibelle', 'offresManqueCandidats', 'experienceCommentaire','langues','contact_urlPostulation', 'lieuTravail_codePostal','contact_coordonnees2', 'contact_coordonnees3', 'agence_courriel','contact_courriel', 'complementExercice'])

#new_df.to_csv('test.csv')
print(new_df.head(5))

#print(salary_by_enterprise.columns)
if_exists = 'replace'

with engine.connect() as con:
 new_df.to_sql(
 name="Job3", 
 con=con ,
 if_exists=if_exists
 )
print(new_df.dtypes)

