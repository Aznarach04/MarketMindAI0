import { useState } from "react";

export default function MarketMindAI() {
  const [productDescription, setProductDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!productDescription) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://ton-backend.onrender.com/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_description: productDescription })
      });

      const data = await response.json();
      setResult(data.market_analysis);
    } catch (error) {
      setResult("Erreur lors de l'analyse du marché.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>MarketMindAI</h1>
      <p>Testez votre produit avant son lancement.</p>
      <textarea
        value={productDescription}
        onChange={(e) => setProductDescription(e.target.value)}
        placeholder="Décrivez votre produit..."
      />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyse en cours..." : "Analyser le marché"}
      </button>
      {result && <p><strong>Résultat :</strong> {result}</p>}
    </div>
  );
}
