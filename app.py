from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes du frontend

openai.api_key = "TON_API_KEY_OPENAI"

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    product_description = data.get("product_description", "").strip()

    if not product_description:
        return jsonify({"error": "Veuillez fournir une description du produit"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en études de marché."},
                {"role": "user", "content": product_description}
            ]
        )
        result = response["choices"][0]["message"]["content"]
        return jsonify({"market_analysis": result})

    except Exception as e:
        return jsonify({"error": f"Erreur OpenAI : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
