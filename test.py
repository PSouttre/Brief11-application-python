import requests
from offres_emploi import Api

client = Api(client_id="", 
             client_secret="")

from offres_emploi.utils import dt_to_str_iso
import datetime

start_dt = datetime.datetime(2020, 3, 1, 12, 30)
end_dt = datetime.datetime.today()
params = {
    "motsCles": "data science",
    'minCreationDate': dt_to_str_iso(start_dt),
    'maxCreationDate': dt_to_str_iso(end_dt)
}
search_on_big_data = client.search(params=params)

import pandas as pd
results =  search_on_big_data['resultats']

results_df = pd.DataFrame(results)
salary_by_enterprise = (
 results_df[['entreprise', 'salaire']]
 .dropna()
 .agg(dict(entreprise=lambda x: x.get('nom'),
           salaire=lambda x: x.get('commentaire')))
 .dropna(subset=["salaire"])
 .loc[lambda df: df.salaire.str.contains("\d+")]
 .sort_values("salaire")
)

print(results_df)