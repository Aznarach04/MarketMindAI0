from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

import os
openai.api_key = os.getenv("OPENAI_API_KEY")


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
                {"role": "system", "content": "Tu es un expert en études de marché et en psychologie du consommateur."},
                {"role": "user", "content": product_description},
            ]
        )
        result = response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"Erreur OpenAI: {str(e)}"}), 500

    return jsonify({"market_analysis": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

