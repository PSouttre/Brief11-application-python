import os 
import json
import pandas as pd 
from dotenv import load_dotenv
from openai import AzureOpenAI
from sqlalchemy import create_engine
import requests

DB_URL = ("postgresql://PS:Password@localhost/PS" )
engine = create_engine(DB_URL)

print(load_dotenv())

AZUR_ENDPOINT = os.getenv("AZUR_ENDPOINT")
AZUR_KEY = os.getenv("AZUR_KEY")

query = 'SELECT * FROM "Job5";'  
with engine.connect() as connection:
    df = pd.read_sql(query, connection)
print(df.shape)


#print(df.shape)

client = AzureOpenAI(
    api_key=AZUR_KEY,  
    api_version="2024-10-21",
    azure_endpoint=AZUR_ENDPOINT
    )

deployment_name="gpt-35-turbo"

#completion = client.chat.completions.create(
#    model=deployment_name,  # e.g. gpt-35-instant
#    messages=[
#       {
#            "role": "assistant",
#            "content": "How do I output all files in a directory using Python?",
 #       },
 #   ],
#)

job_description = df.loc[df['description']]

#print(job_description)
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

    response = completion.choices[0].message.content
    data = json.loads(response)
     
    data.to_csv("test.csv")

    return data.get("Hard skill", []), data.get("Soft skill", []), data.get("Technologie", [])
