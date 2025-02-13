from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialiser l'application Flask
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes depuis le frontend

# Vérifier et charger la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("La clé API OpenAI est manquante. Configurez-la dans les variables d'environnement.")

@app.route("/", methods=["GET"])
def home():
    """Route d'accueil pour vérifier que l'API est en ligne"""
    return "Bienvenue sur MarketMindAI Backend", 200

@app.route("/simulate", methods=["POST"])
def simulate():
    """Route pour analyser un produit via OpenAI"""
    try:
        # Récupérer les données envoyées en JSON
        data = request.get_json()
        product_description = data.get("product_description", "").strip()

        # Vérifier si la description est bien fournie
        if not product_description:
            return jsonify({"error": "Veuillez fournir une description du produit"}), 400

        # Envoyer la requête à OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en études de marché et en psychologie du consommateur."},
                {"role": "user", "content": product_description},
            ]
        )

        # Extraire et retourner le résultat
        result = response["choices"][0]["message"]["content"]
        return jsonify({"market_analysis": result})

    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'analyse du marché : {str(e)}"}), 500

# Définir le port correctement pour Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render utilise 5000 par défaut
    app.run(host="0.0.0.0", port=port)

