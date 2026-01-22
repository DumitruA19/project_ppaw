import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AuthProvider } from "@/auth/AuthContext";
import ProtectedRoute from "@/auth/ProtectedRoute";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";

import LoginPage from "@/pages/Login";
import RegisterPage from "@/pages/Register";
import ChatPage from "@/pages/Chat";
import PlansPage from "@/pages/Plans";
import AccountPage from "@/pages/Account";
import ForgotPassword from "@/pages/ForgotPassword";
import ResetPassword from "@/pages/ResetPassword";
import AdminPage from "@/pages/AdminPage";

function Shell() {
  const location = useLocation();

  // 🔓 Pagini de autentificare (fără Navbar sau Sidebar)
  const isAuthPage = ["/login", "/register", "/forgot-password", "/reset-password"].includes(location.pathname);

  // 👑 Pagina de Admin (își gestionează singură Sidebar/Navbar intern)
  const isAdminPage = location.pathname.startsWith("/admin");

  // Logică pentru ascunderea elementelor globale
  const hideGlobalSidebar = isAuthPage || isAdminPage;
  const hideGlobalNavbar = isAuthPage || isAdminPage;

  return (
    <div className="flex bg-slate-950 min-h-screen">
      {/* 1. Sidebar Global: Afișat doar pe paginile de user (Chat, Account, Plans) */}
      {!hideGlobalSidebar && <Sidebar />}

      <main
        className={
          hideGlobalSidebar
            ? "w-full"
            : "flex-1 ml-60 bg-slate-950 text-gray-100 min-h-screen transition-all duration-300"
        }
      >
        {/* 2. Navbar Global: Afișat doar pe paginile de user */}
        {!hideGlobalNavbar && <Navbar />}

        <Routes>
          {/* 🔁 Redirect default */}
          <Route path="/" element={<Navigate to="/chat" replace />} />

          {/* 🌍 Rute Publice */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />

          {/* 👥 Rute User Protejate */}
          <Route
            path="/chat"
            element={
              <ProtectedRoute requirePlan>
                <ChatPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/plans"
            element={
              <ProtectedRoute>
                <PlansPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/account"
            element={
              <ProtectedRoute>
                <AccountPage />
              </ProtectedRoute>
            }
          />

          {/* 👑 Ruta Admin Protejată (Verifică rolul de admin) */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute requireAdmin>
                <AdminPage />
              </ProtectedRoute>
            }
          />

          {/* 🧱 Fallback 404 */}
          <Route 
            path="*" 
            element={
              <div className="flex items-center justify-center h-full text-slate-500">
                <div className="text-center">
                  <h2 className="text-4xl font-bold mb-2">404</h2>
                  <p>Pagina solicitată nu a fost găsită.</p>
                </div>
              </div>
            } 
          />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Shell />
      </BrowserRouter>
    </AuthProvider>
  );
}