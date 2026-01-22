import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";

// src/auth/ProtectedRoute.jsx
export default function ProtectedRoute({ children, requireAdmin = false }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) return <div>Se încarcă...</div>;

  // DEBUG: Vezi ce rol are user-ul tău în consolă (F12)
  console.log("Utilizator curent în ProtectedRoute:", user);

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requireAdmin && user.role !== "admin") {
    console.warn("Acces refuzat: Rolul tău este", user.role);
    return <Navigate to="/chat" replace />;
  }

  return children;
}