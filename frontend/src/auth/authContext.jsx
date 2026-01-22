import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { login as apiLogin } from "@/api/auth";
import { fetchProfile, fetchOverview } from "@/api/account";

const AuthCtx = createContext();

export function useAuth() {
  return useContext(AuthCtx);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [plan, setPlan] = useState(null);
  const [usage, setUsage] = useState(null);

  // 1. Funcție pentru a încărca overview-ul (plan, usage)
  const refreshOverview = useCallback(async () => {
    try {
      const data = await fetchOverview();
      setPlan(data.subscription || null);
      setUsage(data.usage || null);
    } catch (err) {
      setPlan(null);
      setUsage(null);
    }
  }, []);

  // 2. Funcție pentru a încărca profilul complet
  const loadProfile = useCallback(async () => {
    try {
      const u = await fetchProfile();
      setUser(u);
      await refreshOverview();
      return u;
    } catch (err) {
      setUser(null);
      throw err;
    }
  }, [refreshOverview]);

  // 3. Funcție pentru refresh sesiune (la încărcarea paginii)
  const refresh = useCallback(async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      await loadProfile();
    } catch (err) {
      console.warn("Sesiune neautorizată la refresh");
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
    } finally {
      setLoading(false);
    }
  }, [loadProfile]);

  // 4. Funcția de Login
  async function login(email, password) {
    try {
      const res = await apiLogin(email, password);
      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("role", res.role);

      const u = await loadProfile();
      setLoading(false);
      return u.role;
    } catch (err) {
      setLoading(false);
      throw new Error(err.response?.data?.detail || "Login failed");
    }
  }

  // 5. FUNCȚIA LOGOUT (Aceasta lipsea și cauza eroarea)
  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    setUser(null);
    setPlan(null);
    setUsage(null);
    // Opțional: Redirecționare forțată
    window.location.href = "/login";
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <AuthCtx.Provider value={{ 
      user, 
      loading, 
      plan, 
      usage, 
      login, 
      logout, // Acum logout este definit!
      refresh, 
      refreshOverview 
    }}>
      {children}
    </AuthCtx.Provider>
  );
}