from flask import Flask, jsonify
from pymongo import MongoClient
import os
import requests

app = Flask(__name__)

db_uri = "mongodb+srv://Yildirim:Yildirim31@cluster0.4ij4k.mongodb.net/"
client = MongoClient(db_uri)

@app.route('/api/data')
def get_data():
    api_url = 'https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search'
    headers = {
        'Authorization': 'Bearer vc6fhJrDgS9QcRPIXH07-V_I9cY'
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "error": "Impossible de contacter l'API externe",
            "status_code": response.status_code,
            "response_text": response.text,
            "response_headers": dict(response.headers)
        }), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
