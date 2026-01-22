import { useState } from "react";
import axios from "../api/client";
import { createSubscription } from "@/api/subscription"; // IMPORT NOU

export default function PaymentForm({ plan, onClose }) {
  const [cardNumber, setCardNumber] = useState("");
  const [expDate, setExpDate] = useState("");
  const [cvv, setCvv] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // src/components/PaymentForm.jsx

const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setLoading(true);
  try {
    // 1. Apelăm checkout cu datele de preț pentru tabelul 'payments'
    await axios.post("/subscriptions/checkout", { 
      amount: plan.price_cents, // Backend-ul împarte la 100
      currency: plan.currency 
    }); 
    
    // 2. Activăm abonamentul
    await createSubscription(plan.code); 
    
    alert(`Plata pentru ${plan.name} a fost simulată cu succes!`);
    onClose();
    window.location.reload();
  } catch (err) {
    setError(err.response?.data?.detail || "Eroare la procesarea plății.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center z-50">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 text-gray-100 p-8 rounded-2xl shadow-2xl w-full max-w-md space-y-6 border border-slate-700"
      >
        <h2 className="text-2xl font-bold text-center">
          Plătește: <span className="text-blue-400">{plan.name}</span>
        </h2>

        <p className="text-center text-gray-400">
          {(plan.price_cents / 100).toFixed(2)} {plan.currency} / {plan.period}
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Număr card</label>
            <input
              type="text"
              required
              maxLength="19"
              placeholder="1234 5678 9012 3456"
              value={cardNumber}
              onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, "").replace(/(.{4})/g, "$1 ").trim())}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
            />
          </div>

          <div className="flex gap-3">
            <div className="flex-1">
              <label className="block text-sm text-gray-400 mb-1">Expiră (MM/YY)</label>
              <input
                type="text"
                required
                placeholder="MM/YY"
                value={expDate}
                onChange={(e) => setExpDate(e.target.value.replace(/\D/g, "").replace(/(\d{2})(\d{1,2})/, "$1/$2").substr(0, 5))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
              />
            </div>

            <div className="w-24">
              <label className="block text-sm text-gray-400 mb-1">CVV</label>
              <input
                type="password"
                required
                maxLength="3"
                placeholder="123"
                value={cvv}
                onChange={(e) => setCvv(e.target.value.replace(/\D/g, ""))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
              />
            </div>
          </div>
        </div>

        {error && (
          <div className="text-red-400 text-sm bg-red-900/30 p-2 rounded-md border border-red-700">{error}</div>
        )}

        <div className="flex justify-between items-center mt-4">
          <button type="button" onClick={onClose} className="px-5 py-2 border border-slate-600 text-gray-300 rounded-lg hover:bg-slate-800 transition">
            Anulează
          </button>
          <button type="submit" disabled={loading} className={`px-6 py-2 rounded-lg font-semibold text-white shadow ${loading ? "bg-gray-600 cursor-not-allowed" : "bg-green-600 hover:bg-green-700 transition"}`}>
            {loading ? "Se procesează..." : "Plătește"}
          </button>
        </div>
      </form>
    </div>
  );
}