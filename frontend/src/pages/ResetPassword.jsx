import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from "@/api/client";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const token = params.get("token");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/auth/reset-password", {
        token,
        new_password: password,
      });
      setMsg(res.data.message);
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setMsg(err.response?.data?.detail || "Eroare la resetare.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 p-8 rounded-2xl shadow-lg w-full max-w-md space-y-4 border border-slate-700"
      >
        <h1 className="text-2xl font-bold text-center text-blue-400">
          Resetare parolă
        </h1>
        <p className="text-sm text-gray-400 text-center">
          Introdu o parolă nouă pentru contul tău.
        </p>

        <input
          type="password"
          placeholder="Parola nouă"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
        />

        <button
          type="submit"
          className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg py-2"
        >
          Resetează parola
        </button>

        {msg && (
          <p className="text-sm text-center mt-2 text-green-400">{msg}</p>
        )}
      </form>
    </div>
  );
}
