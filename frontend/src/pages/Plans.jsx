// src/pages/PlansPage.jsx
import { useState } from "react";
import { createSubscription } from "@/api/subscription";
import PaymentForm from "@/components/PaymentForm";

export default function PlansPage() {
  const [plans] = useState([
    {
      id: 1,
      code: "FREE",
      name: "Free",
      price_cents: 0,
      currency: "EUR",
      period: "lună",
      features: ["5 recomandări/lună", "Acces la baza de date de bază", "Timp de răspuns standard"],
      color: "border-slate-700"
    },
    {
      id: 2,
      code: "STANDARD",
      name: "Standard",
      price_cents: 499,
      currency: "EUR",
      period: "lună",
      features: ["100 recomandări/lună", "Acces prioritar la AI", "Istoric conversații salvat", "Suport prin email"],
      color: "border-blue-500/50 shadow-blue-500/10"
    },
    {
      id: 3,
      code: "PREMIUM",
      name: "Premium",
      price_cents: 1499,
      currency: "EUR",
      period: "lună",
      features: ["Încercări nelimitate", "Recomandări ultra-personalizate", "Analiză avansată de context", "Suport 24/7"],
      color: "border-fuchsia-500/50 shadow-fuchsia-500/10"
    },
  ]);

  const [selectedPlan, setSelectedPlan] = useState(null);
  const [message, setMessage] = useState({ text: "", isError: false });

  // Funcție doar pentru activarea planului GRATUIT
  async function handleActivateFree() {
    setMessage({ text: "Se activează planul gratuit...", isError: false });
    try {
      await createSubscription("FREE");
      setMessage({ text: "✅ Planul Free a fost activat cu succes!", isError: false });
    } catch (e) {
      setMessage({ text: e.response?.data?.detail || "Eroare la activare.", isError: true });
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-black mb-4">Alege planul potrivit</h1>
          <p className="text-slate-400">Deblochează puterea AI pentru biblioteca ta personală.</p>
        </header>

        <div className="grid md:grid-cols-3 gap-8">
          {plans.map((p) => (
            <div key={p.id} className={`flex flex-col border ${p.color} p-8 rounded-3xl bg-slate-900/50 backdrop-blur-sm shadow-2xl transition hover:scale-105`}>
              <h2 className="text-2xl font-bold mb-2">{p.name}</h2>
              <div className="mb-6">
                <span className="text-4xl font-black">{p.price_cents / 100} {p.currency}</span>
                <span className="text-slate-500 ml-2">/ {p.period}</span>
              </div>

              <ul className="space-y-4 mb-8 flex-1">
                {p.features.map((f, i) => (
                  <li key={i} className="flex items-center text-sm text-slate-300">
                    <span className="mr-2 text-green-500">✔</span> {f}
                  </li>
                ))}
              </ul>

              <button
                onClick={() => {
                  if (p.code === "FREE") handleActivateFree();
                  else setSelectedPlan(p); // Deschide modalul de plată pentru planuri cu bani
                }}
                className={`w-full py-3 rounded-xl font-bold transition ${
                  p.code === "FREE" 
                  ? "bg-slate-800 hover:bg-slate-700" 
                  : "bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-600/20"
                }`}
              >
                {p.code === "FREE" ? "Începe gratuit" : "Activează acum"}
              </button>
            </div>
          ))}
        </div>

        {/* MODALUL DE PLATĂ */}
        {selectedPlan && (
          <PaymentForm 
            plan={selectedPlan} 
            onClose={() => setSelectedPlan(null)} 
          />
        )}

        {message.text && (
          <div className={`mt-10 p-4 rounded-xl border text-center ${
            message.isError ? "bg-red-900/20 border-red-500/50 text-red-400" : "bg-green-900/20 border-green-500/50 text-green-400"
          }`}>
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
}