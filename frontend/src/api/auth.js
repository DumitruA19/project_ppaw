// src/api/auth.js
import api from "./client";

export async function register(payload) {
  // Payload conține { email, password, name, role }
  const { data } = await api.post("/auth/register", payload);
  return data;
}

export async function login(email, password) {
  // REPARAȚIE 422: FastAPI OAuth2 așteaptă 'application/x-www-form-urlencoded'
  const formData = new URLSearchParams();
  formData.append("username", email); // Email-ul trece drept 'username'
  formData.append("password", password);

  const { data } = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  // Data va conține { access_token, token_type, role }
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
}