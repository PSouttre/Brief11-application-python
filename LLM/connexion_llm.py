import os 
import pandas as pd 
from dotenv import load_dotenv
from openai import AzureOpenAI
from sqlalchemy import create_engine
import requests

DB_URL = ("postgresql://username:password@localhost/nomdetadatabase" )
engine = create_engine(DB_URL)

print(load_dotenv())

AZUR_ENDPOINT = os.getenv("AZUR_ENDPOINT")
AZUR_KEY = os.getenv("AZUR_KEY")

query = 'SELECT * FROM "nomdelatable";'  
with engine.connect() as connection:
    df = pd.read_sql(query, connection)



#print(df.shape)

client = AzureOpenAI(
    api_key=AZUR_KEY,  
    api_version="2024-10-21",
    azure_endpoint=AZUR_ENDPOINT
    )

deployment_name="gpt-35-turbo"

#completion = client.chat.completions.create(
    #model=deployment_name,  # e.g. gpt-35-instant
   # messages=[
     #   {
    #        "role": "assistant",
   #         "content": "How do I output all files in a directory using Python?",
  #      },
 #   ],
#)
#print(completion)





#print(job_description)
for idx, job_description in enumerate(df["description"]):
    prompt = f"""
    Ta tâche est d'extraire des compétences mentionnées dans une offre d'emploi. Ton objectif est d'extraire et de catégoriser ces compétences sous format JSON.
    Extrait les compétences selon le schéma suivant: {{category1: [compétence1, compétence2, etc.], category2: [compétence3, compétence4, etc.]}}. 
    Assume everything mentioned refers to the same thing. 
    The extracted information should be categorized according to the allowed categories specified below.

    Constraints:
      - Allowed Categories: "Hard skill", "Soft skill", "Technologie"
     
    Input: {job_description}
    Output:
    """
    print(f"Prompt for job {idx}:\n{prompt}\n")
  