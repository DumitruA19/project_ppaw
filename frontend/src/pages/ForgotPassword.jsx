import { useState } from "react";
import axios from "@/api/client";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      const res = await axios.post("/auth/forgot-password", { email });
      setMsg(res.data.message);
    } catch (err) {
      setMsg(err.response?.data?.detail || "Eroare la trimiterea cererii.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 p-8 rounded-2xl shadow-lg w-full max-w-md space-y-4 border border-slate-700"
      >
        <h1 className="text-2xl font-bold text-center text-blue-400">
          Recuperare parolă
        </h1>
        <p className="text-sm text-gray-400 text-center">
          Introdu adresa ta de email și îți vom trimite un link de resetare.
        </p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg py-2"
        >
          Trimite linkul
        </button>

        {msg && (
          <p className="text-sm text-center mt-2 text-green-400">{msg}</p>
        )}

        <button
          type="button"
          onClick={() => navigate("/login")}
          className="text-sm text-blue-400 hover:underline w-full text-center mt-4"
        >
          Înapoi la autentificare
        </button>
      </form>
    </div>
  );
}
