// import { useEffect, useState } from "react";
// import { login, me } from "@/api/auth";
// import { useAuth } from "@/auth/AuthContext";
// import { useNavigate, Link } from "react-router-dom";

// export default function LoginPage() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [err, setErr] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const { refresh } = useAuth();
//   const nav = useNavigate();

//   useEffect(() => {
//     me().then(() => nav("/chat", { replace: true })).catch(() => {});
//   }, [nav]);

//   async function onSubmit(e) {
//     e.preventDefault();
//     setErr(null); setLoading(true);
//     try {
//       await login(email, password);
//       await refresh();
//       nav("/chat", { replace: true });
//     } catch (e) {
//       setErr(e?.response?.data?.detail ?? "Login failed");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="min-h-screen grid place-items-center p-6">
//       <div className="container">
//         <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
//           {/* Side hero cu titlu & text frumos */}
//           <section className="hidden md:block">
//             <h1 className="text-4xl md:text-5xl font-black leading-tight">
//               Welcome back <span className="inline-block">👋</span>
//             </h1>
//             <p className="text-slate-300 mt-4 text-lg max-w-md">
//               Sign in to get <span className="text-cyan-300 font-semibold">vivid</span>, AI-powered book recommendations,
//               tuned to your mood and favorite genres.
//             </p>
//           </section>

//           {/* Card login */}
//           <section className="card p-6 md:p-8">
//             <h2 className="text-xl font-semibold mb-2">Sign in</h2>
//             <p className="text-sm text-slate-300 mb-6">Use your account to access the chat.</p>

//             <form onSubmit={onSubmit} className="grid gap-4">
//               <input
//                 className="input"
//                 placeholder="Email"
//                 type="email"
//                 value={email}
//                 onChange={(e)=>setEmail(e.target.value)}
//               />
//               <input
//                 className="input"
//                 placeholder="Password"
//                 type="password"
//                 value={password}
//                 onChange={(e)=>setPassword(e.target.value)}
//               />

//               <button className="btn btn-primary" disabled={loading}>
//                 {loading ? "Signing in…" : "Sign in"}
//               </button>

//               {err && <div className="text-red-400 text-sm">{String(err)}</div>}

//               <div className="text-sm text-slate-300">
//                 Don’t have an account?{" "}
//                 <Link className="underline decoration-cyan-400" to="/register">Create one</Link>
//               </div>
//             </form>
//           </section>
//         </div>
//       </div>
//     </div>
//   );
// }

// src/pages/Login.jsx
// src/pages/Login.jsx
import { useEffect, useState } from "react";
import { login } from "@/api/auth";
import { fetchProfile } from "@/api/account";
import { useAuth } from "@/auth/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);
  const { refresh } = useAuth();
  const nav = useNavigate();

  // 🔁 Dacă deja e logat, redirecționează spre chat
  useEffect(() => {
    fetchProfile()
      .then(() => nav("/chat", { replace: true }))
      .catch(() => {}); // ignoră eroarea 401
  }, [nav]);

  // 🔐 Login
  async function onSubmit(e) {
    e.preventDefault();
    setErr(null);
    setLoading(true);

    try {
      const res = await login(email, password);

      // Salvează token-ul JWT
      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("role", res.role);

      // Reîmprospătează contextul global
      await refresh();

      // Redirecționează în funcție de rol
      if (res.role === "admin") {
        nav("/admin", { replace: true });
      } else {
        nav("/chat", { replace: true });
      }
    } catch (e) {
      setErr(e?.response?.data?.detail ?? "Autentificare eșuată.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen grid place-items-center p-6 bg-slate-950 text-gray-100">
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          {/* 🧠 Partea stângă - mesaj de întâmpinare */}
          <section className="hidden md:block">
            <h1 className="text-4xl md:text-5xl font-black leading-tight">
              Bine ai revenit <span className="inline-block">👋</span>
            </h1>
            <p className="text-slate-300 mt-4 text-lg max-w-md">
              Autentifică-te pentru a primi{" "}
              <span className="text-cyan-300 font-semibold">recomandări AI</span>{" "}
              personalizate în funcție de starea ta de spirit și genurile
              preferate.
            </p>
          </section>

          {/* 🔐 Cardul de login */}
          <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-lg">
            <h2 className="text-xl font-semibold mb-2 text-blue-400">
              Autentificare
            </h2>
            <p className="text-sm text-slate-400 mb-6">
              Folosește contul tău pentru a accesa Smart Librarian.
            </p>

            <form onSubmit={onSubmit} className="grid gap-4">
              <input
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
                placeholder="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 outline-none text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-400 transition"
                placeholder="Parolă"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              <button
                className="w-full bg-blue-600 hover:bg-blue-700 rounded-lg py-2 font-semibold text-white transition disabled:opacity-50"
                disabled={loading}
              >
                {loading ? "Se autentifică…" : "Autentificare"}
              </button>

              {err && (
                <div className="text-red-400 text-sm mt-2 text-center">
                  {String(err)}
                </div>
              )}

              <div className="flex flex-col md:flex-row justify-between text-sm text-slate-300 mt-2 space-y-2 md:space-y-0">
                <div>
                  Nu ai cont?{" "}
                  <Link
                    className="underline decoration-cyan-400 hover:text-cyan-300"
                    to="/register"
                  >
                    Creează unul
                  </Link>
                </div>
                <div>
                  <Link
                    to="/forgot-password"
                    className="text-blue-400 hover:text-blue-300 underline"
                  >
                    Ai uitat parola?
                  </Link>
                </div>
              </div>
            </form>
          </section>
        </div>
      </div>
    </div>
  );
}
