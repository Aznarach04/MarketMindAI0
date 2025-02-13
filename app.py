from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

app.config["DEBUG"] = True

# ✅ Vérification de la clé API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ ERREUR: Clé API OpenAI absente ! Ajoutez-la dans Render.")
else:
    openai.api_key = api_key

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue sur MarketMindAI API"})

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json()
        print(f"📩 Requête reçue: {data}")  

        if not data or "product_description" not in data:
            return jsonify({"error": "❌ 'product_description' est manquant"}), 400

        product_description = data["product_description"].strip()
        if not product_description:
            return jsonify({"error": "❌ Description vide"}), 400

        # ✅ Test OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en études de marché."},
                {"role": "user", "content": product_description}
            ]
        )

        result = response["choices"][0]["message"]["content"]
        print(f"✅ Réponse OpenAI: {result}")

        return jsonify({"market_analysis": result})

    except Exception as e:
        print(f"🔥 ERREUR SERVEUR: {str(e)}")  
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
