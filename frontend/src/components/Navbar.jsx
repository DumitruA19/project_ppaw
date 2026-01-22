import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";
import { logout } from "@/api/auth";
import { useEffect, useState } from "react";
import { fetchOverview } from "@/api/account";

export default function Navbar() {
  const { user } = useAuth();
  const nav = useNavigate();
  const [planInfo, setPlanInfo] = useState(null);

  function onLogout() {
    logout();
    nav("/login", { replace: true });
  }

  // 🔄 Încarcă planul curent + usage
  useEffect(() => {
    if (!user) return;
    fetchOverview()
      .then((data) => setPlanInfo(data))
      .catch(() => {});
  }, [user]);

  return (
    <header className="sticky top-0 z-40 backdrop-blur bg-slate-950/60 border-b border-white/10">
      <div className="container h-16 flex items-center justify-between text-gray-100">
        <Link to="/chat" className="flex items-center gap-3">
          <div className="size-9 rounded-[14px] bg-gradient-to-tr from-cyan-400 to-fuchsia-500 grid place-items-center">
            📚
          </div>
          <div className="leading-tight">
            <div className="font-semibold tracking-wide text-lg"></div>
            <div className="text-xs text-gray-400">AI Book Assistant</div>
          </div>
        </Link>

        <nav className="flex items-center gap-3 text-sm">
          {planInfo && planInfo.subscription ? (
            <div className="bg-slate-800/50 px-3 py-1.5 rounded-md border border-slate-700 flex items-center gap-2">
              <span className="text-cyan-400 font-semibold">
                {planInfo.subscription.status === "active"
                  ? planInfo.subscription.plan
                  : "Fără plan activ"}
              </span>
              <span className="text-gray-400">|</span>
              <span className="text-gray-300">
                {planInfo.usage?.messages_used ?? 0} mesaje
              </span>
            </div>
          ) : (
            <div className="text-gray-400 text-sm">Plan: —</div>
          )}

          <Link to="/account" className="btn btn-ghost">
            Contul meu
          </Link>
          <button onClick={onLogout} className="btn btn-primary">
            Ieșire
          </button>
        </nav>
      </div>
    </header>
  );
}
