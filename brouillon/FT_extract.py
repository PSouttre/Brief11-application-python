import os

import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")    # permet de récupérer une variable d'environnement à partir du système d'exploitation
AZURE_KEY = os.getenv("AZURE_KEY")


client = AzureOpenAI(
    api_key=AZURE_KEY,  
    api_version="2024-11-28",
    azure_endpoint=AZURE_ENDPOINT
    )