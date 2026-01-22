import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchProfile, changePassword, fetchOverview } from "@/api/account";

export default function AccountPage() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [overview, setOverview] = useState(null);
  const [oldPass, setOldPass] = useState("");
  const [newPass, setNewPass] = useState("");
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [p, o] = await Promise.all([fetchProfile(), fetchOverview()]);
        setProfile(p);
        setOverview(o);
      } catch (err) {
        console.error("[Account] load error:", err);
      }
    })();
  }, []);

  // src/pages/Account.jsx
const onChangePassword = async (e) => {
  e.preventDefault();
  setSaving(true);
  setMsg("");
  try {
    // Trimitem direct valorile din state
    await changePassword(oldPass, newPass); 
    setMsg("✅ Parola a fost schimbată cu succes.");
    setOldPass("");
    setNewPass("");
  } catch (err) {
    // Afișăm eroarea venită din backend (400 Bad Request)
    setMsg(err.response?.data?.detail || "❌ Eroare la schimbarea parolei.");
  } finally {
    setSaving(false);
  }
};

  // Calculăm statisticile de utilizare extrase din backend
  const stats = (() => {
    if (!overview?.subscription) return { used: 0, limit: 5, percent: 0, isNearLimit: false };
    
    const used = overview.subscription.messages_used || 0;
    const limit = overview.subscription.messages_limit; // Din PLAN_LIMITS
    
    if (limit === null) return { used, limit: "Nelimitat", percent: 100, isNearLimit: false };
    
    const percent = Math.min((used / limit) * 100, 100);
    return { 
      used, 
      limit, 
      percent, 
      isNearLimit: percent >= 80 // Alertă la peste 80%
    };
  })();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-gray-100 p-6 space-y-8">
      <header className="flex justify-between items-center border-b border-slate-700 pb-4">
        <h1 className="text-3xl font-bold text-white">Gestionare Cont</h1>
        <button 
          onClick={() => navigate("/plans")}
          className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg text-sm font-bold transition-all shadow-lg shadow-blue-600/20"
        >
          Vezi Planuri
        </button>
      </header>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* COLOANA 1: PROFIL SI SECURITATE */}
        <div className="lg:col-span-1 space-y-8">
          <section className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700 backdrop-blur-md">
            <h2 className="text-lg font-semibold mb-4 text-blue-400">Informații Profil</h2>
            {profile ? (
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-slate-500 font-bold uppercase">Nume</label>
                  <p className="text-gray-100">{profile.name || "Utilizator Smart"}</p>
                </div>
                <div>
                  <label className="text-xs text-slate-500 font-bold uppercase">Email</label>
                  <p className="text-gray-100">{profile.email}</p>
                </div>
                <div>
                  <label className="text-xs text-slate-500 font-bold uppercase">Membru din</label>
                  <p className="text-gray-100">{new Date(profile.created_at).toLocaleDateString()}</p>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 italic">Se încarcă profilul...</div>
            )}
          </section>

          <section className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700">
            <h2 className="text-lg font-semibold mb-4 text-blue-400">Securitate</h2>
            <form onSubmit={onChangePassword} className="space-y-4">
              <input
                type="password"
                placeholder="Parola curentă"
                className="w-full bg-slate-900 border border-slate-700 p-3 rounded-lg outline-none focus:border-blue-500 transition"
                value={oldPass}
                onChange={(e) => setOldPass(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Parola nouă"
                className="w-full bg-slate-900 border border-slate-700 p-3 rounded-lg outline-none focus:border-blue-500 transition"
                value={newPass}
                onChange={(e) => setNewPass(e.target.value)}
                required
                minLength={8}
              />
              <button
                type="submit"
                disabled={saving}
                className="w-full bg-slate-700 hover:bg-slate-600 py-2 rounded-lg font-bold transition disabled:opacity-50"
              >
                {saving ? "Se salvează..." : "Schimbă Parola"}
              </button>
              {msg && <p className="text-xs text-center mt-2">{msg}</p>}
            </form>
          </section>
        </div>

        {/* COLOANA 2: ABONAMENT SI CONSUM (MAI MARE) */}
        <div className="lg:col-span-2 space-y-8">
          <section className="bg-slate-800/80 rounded-3xl p-8 border border-slate-700 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10">
                <svg width="100" height="100" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </div>

            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <span className="w-2 h-6 bg-blue-500 rounded-full"></span>
              Stare Abonament
            </h2>

            {overview?.subscription ? (
              <div className="space-y-8">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-4xl font-black text-white uppercase tracking-tighter">
                      {overview.subscription.plan}
                    </h3>
                    <p className="text-slate-400 mt-1">
                      Status: <span className="text-green-400 font-bold uppercase text-xs">{overview.subscription.status}</span>
                    </p>
                  </div>
                  {overview.subscription.plan !== "PREMIUM" && (
                    <button 
                      onClick={() => navigate("/plans")}
                      className="bg-gradient-to-r from-blue-600 to-fuchsia-600 px-6 py-3 rounded-xl font-black text-white hover:scale-105 transition active:scale-95 shadow-xl shadow-blue-500/20"
                    >
                      UPGRADE NOW
                    </button>
                  )}
                </div>

                <div className="space-y-4 bg-slate-900/50 p-6 rounded-2xl border border-slate-700">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-bold text-slate-300">Mesaje AI utilizate</span>
                    <span className={`text-lg font-mono font-bold ${stats.isNearLimit ? 'text-red-400' : 'text-blue-400'}`}>
                      {stats.used} / {stats.limit}
                    </span>
                  </div>

                  {/* Progres vizual */}
                  <div className="w-full bg-slate-800 h-4 rounded-full overflow-hidden p-1 border border-slate-700">
                    <div 
                      className={`h-full rounded-full transition-all duration-1000 ${
                        stats.isNearLimit ? 'bg-gradient-to-r from-red-600 to-orange-500' : 'bg-gradient-to-r from-blue-600 to-cyan-400'
                      }`}
                      style={{ width: `${stats.percent}%` }}
                    ></div>
                  </div>

                  {stats.isNearLimit && (
                    <p className="text-xs text-red-400 font-bold animate-pulse">
                      ⚠️ Atenție: Te apropii de limita planului tău!
                    </p>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-900/30 p-4 rounded-xl border border-slate-800">
                        <p className="text-[10px] text-slate-500 uppercase font-bold">Următoarea facturare</p>
                        <p className="text-sm text-slate-200">{new Date(overview.subscription.current_period_end).toLocaleDateString()}</p>
                    </div>
                    <div className="bg-slate-900/30 p-4 rounded-xl border border-slate-800">
                        <p className="text-[10px] text-slate-500 uppercase font-bold">Tip Ciclu</p>
                        <p className="text-sm text-slate-200">Lunar</p>
                    </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-10">
                <p className="text-slate-500 mb-4">Nu am găsit un abonament activ.</p>
                <button onClick={() => navigate("/plans")} className="text-blue-400 font-bold underline">Alege un plan acum</button>
              </div>
            )}
          </section>

          {/* ALTE STATISTICI */}
          {overview?.usage && (
            <div className="grid grid-cols-2 gap-6">
               <div className="bg-slate-800/40 p-6 rounded-2xl border border-slate-700 text-center">
                  <p className="text-3xl font-black text-white">{overview.usage.tts_seconds}s</p>
                  <p className="text-xs text-slate-500 uppercase font-bold">Text-to-Speech</p>
               </div>
               <div className="bg-slate-800/40 p-6 rounded-2xl border border-slate-700 text-center">
                  <p className="text-3xl font-black text-white">{overview.usage.stt_seconds}s</p>
                  <p className="text-xs text-slate-500 uppercase font-bold">Speech-to-Text</p>
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}