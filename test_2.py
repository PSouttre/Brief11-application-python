###########################################################
################# tout les imports standard ################
###########################################################
import datetime
import re 

###########################################################
################ modules externes #########################
###########################################################
import requests
from offres_emploi import Api
import pandas as pd
from collections.abc import MutableMapping
from offres_emploi.utils import dt_to_str_iso
from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine


###########################################################
################ s'identifier a l'api #####################
###########################################################

client = Api(client_id="", 
             client_secret="")

###########################################################
################ s'identifier a la database ###############
###########################################################

engine = create_engine("postgresql://******:********@*******/*****" )


###########################################################
################ Faire une requetes a l'api ###############
###########################################################


start_dt = datetime.datetime(2019, 3, 1, 12, 30) # Ici nous demondons que les annonces depuis une date demande 
end_dt = datetime.datetime.today()
params = {
    # Nous demandons a l'api de nous sortir que les codeRome ci-dessous 
    "codeROME": ['M1802','M1805','M1810','M1815','M1820', 'M1825', 'M1830', 'M1835'],
    'minCreationDate': dt_to_str_iso(start_dt),
    'maxCreationDate': dt_to_str_iso(end_dt)
}
search_on_big_data = client.search(params=params) # On affecte les parametres 

results =  search_on_big_data['resultats']

###########################################################
################ Applatir les donnees recues ##############
###########################################################

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

###########################################################
################ Filtrer / laver les donnees ##############
###########################################################


# je la met dans une variable pour eviter de toucher a la dataframe de base 
new_df = results_df.drop(columns = ['id','qualitesProfessionnelles','dateCreation','dateActualisation','lieuTravail_latitude','competences', 'lieuTravail_longitude', 'lieuTravail_commune','typeContratLibelle','romeLibelle','appellationlibelle','entreprise_entrepriseAdaptee','typeContratLibelle','lieuTravail_latitude', 'lieuTravail_longitude', 'natureContrat', 'experienceExige','nombrePostes', 'accessibleTH','origineOffre_origine','origineOffre_partenaires','entreprise_description','dureeTravailLibelleConverti','codeNAF','secteurActivite', 'salaire_commentaire','qualificationCode', 'qualificationLibelle','salaire_complement1', 'salaire_complement2','formations','contact_nom','deplacementCode','deplacementLibelle', 'offresManqueCandidats', 'experienceCommentaire','langues','contact_urlPostulation', 'lieuTravail_codePostal','contact_coordonnees2', 'contact_coordonnees3', 'agence_courriel','contact_courriel', 'complementExercice'])

###########################################################
################ L'envoyer vers la BDD ####################
###########################################################

# La variable ci-dessous permet le remplacement des données ou l'ajout de données.
if_exists = 'replace'

with engine.connect() as con:
 new_df.to_sql(
 name="Job3", 
 con=con ,
 if_exists=if_exists
 )
