import openai
import json
import requests
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os

# Configuration API OpenAI (Remplace par ta clé API)
openai.api_key = "your_openai_api_key"

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Initialisation de la base de données SQLite
conn = sqlite3.connect("market_analysis.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_description TEXT,
        market_analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Fonction pour générer un test de marché simulé
def simulate_market(product_description):
    try:
        messages = [
            {"role": "system", "content": "Tu es un expert en études de marché."},
            {"role": "user", "content": f"Analyse ce produit : {product_description}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        logging.error(f"Erreur OpenAI: {str(e)}")
        return f"Erreur lors de la génération de l'analyse : {str(e)}"

# Route API pour simuler le marché et stocker les résultats
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    product_description = data.get("product_description", "").strip()

    if not product_description:
        return jsonify({"error": "Veuillez fournir une description du produit"}), 400

    result = simulate_market(product_description)

    # Stocker le résultat dans la base de données
    cursor.execute("INSERT INTO market_tests (product_description, market_analysis) VALUES (?, ?)", 
                   (product_description, result))
    conn.commit()

    return jsonify({"market_analysis": result})

# Route API pour récupérer les analyses stockées
@app.route("/history", methods=["GET"])
def get_history():
    cursor.execute("SELECT * FROM market_tests ORDER BY created_at DESC")
    rows = cursor.fetchall()
    history = [{"id": row[0], "product_description": row[1], "market_analysis": row[2], "created_at": row[3]} for row in rows]
    return jsonify({"history": history})

# Route API pour tester la connectivité
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Le serveur est opérationnel."})

# Démarrage de l'application Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
