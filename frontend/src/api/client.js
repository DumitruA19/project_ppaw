// src/api/client.js
import axios from "axios";

const api = axios.create({
  // Vite folosește import.meta.env pentru variabilele de mediu
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

// ✅ CORECTAT: Schimbat 'client' în 'api'
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor pentru răspunsuri
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("[Axios] Sesiune expirată sau neautorizată.");
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;