from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configuration de l'API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue sur MarketMindAI API"})

@app.route("/simulate", methods=["POST"])
def simulate_market():
    data = request.get_json()

    if not data or "product_description" not in data:
        return jsonify({"error": "Product description missing"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Remplace par un modèle supporté, ex: gpt-4, gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de marché."},
                {"role": "user", "content": f"Analyse ce produit : {data['product_description']}"}
            ]
        )

        analysis_result = response["choices"][0]["message"]["content"]
        return jsonify({"prediction": analysis_result})

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
