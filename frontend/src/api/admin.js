
import api from "./client";

// ---- USERS ----
export async function getUsers() {
  const { data } = await api.get("/admin/users");
  return data;
}

export async function updateUser(id, payload) {
  // Payload-ul trebuie să conțină: { name: '...', role: '...', password: '...' }
  const { data } = await api.put(`/admin/users/${id}`, payload);
  return data;
}

export async function deleteUser(id) {
  await api.delete(`/admin/users/${id}`);
}

// ---- PLANS ----
export async function getPlans() {
  const { data } = await api.get("/admin/plans");
  return data;
}


export const getActionLogs = async () => {
  // Folosește numele instanței exportate din client.js
  const res = await api.get("/admin/logs"); 
  return res.data;
};

// src/api/admin.js
export async function createUser(payload) {
  const { data } = await api.post("/admin/users", payload);
  return data;
}