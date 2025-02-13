from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Configuration de l'API OpenAI
openai.api_key = os.getenv("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")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue sur MarketMindAI API"}), 200

@app.route("/simulate", methods=["POST"])
def simulate_market():
    try:
        data = request.get_json()
        product_description = data.get("product_description", "")

        if not product_description:
            return jsonify({"error": "La description du produit est requise"}), 400

        # Utilisation de la nouvelle version de l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de marché."},
                {"role": "user", "content": f"Analyse le marché pour : {product_description}"}
            ]
        )

        result = response["choices"][0]["message"]["content"]
        return jsonify({"analysis": result}), 200

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Une erreur interne est survenue", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
