from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("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")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue sur MarketMindAI API"})

@app.route("/simulate", methods=["POST"])
def simulate_market():
    try:
        data = request.get_json()
        product_description = data.get("product_description", "").strip()

        if not product_description:
            return jsonify({"error": "Veuillez fournir une description du produit"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en études de marché et en psychologie du consommateur."},
                {"role": "user", "content": product_description}
            ]
        )

        result = response["choices"][0]["message"]["content"]
        return jsonify({"market_analysis": result})

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la génération de l'analyse : {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
