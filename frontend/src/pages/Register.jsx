// src/pages/Register.jsx
import { useState } from "react";
import { register } from "@/api/auth";
import { Link, useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", name: "", password: "", role: "user" });
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await register(form);
      navigate("/login", { state: { message: "Cont creat cu succes! Te poți autentifica." } });
    } catch (e) {
      setErr(e.response?.data?.detail || "Înregistrarea a eșuat.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-6">
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold text-white mb-2">Creează un cont</h2>
        <p className="text-slate-400 text-sm mb-6">Alătură-te comunității Smart Librarian.</p>

        <form onSubmit={onSubmit} className="space-y-4">
          <input className="w-full bg-slate-800 p-3 rounded-lg outline-none text-white focus:ring-2 focus:ring-blue-500" 
                 placeholder="Nume complet" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
          <input className="w-full bg-slate-800 p-3 rounded-lg outline-none text-white focus:ring-2 focus:ring-blue-500" 
                 placeholder="Email" type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
          <input className="w-full bg-slate-800 p-3 rounded-lg outline-none text-white focus:ring-2 focus:ring-blue-500" 
                 placeholder="Parolă" type="password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required minLength={8} />
          
          <button disabled={loading} className="w-full bg-indigo-600 py-3 rounded-lg font-bold text-white hover:bg-indigo-700 transition">
            {loading ? "Se procesează..." : "Înregistrare"}
          </button>

          {err && <p className="text-red-400 text-sm text-center">{err}</p>}
          <p className="text-center text-slate-500 text-sm mt-4">
            Ai deja cont? <Link to="/login" className="text-indigo-400 underline">Autentifică-te</Link>
          </p>
        </form>
      </div>
    </div>
  );
}