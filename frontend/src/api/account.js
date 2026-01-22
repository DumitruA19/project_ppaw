import api from "./client";

export async function fetchProfile() {
  const { data } = await api.get("/account/me");
  return data; 
}

export async function changePassword(oldPassword, newPassword) {
  const { data } = await api.post("/account/change-password", {
    old_password: oldPassword,
    new_password: newPassword,
  });
  return data;
}

export async function fetchOverview() {
  const { data } = await api.get("/account/overview");
  return data; // Returnează { subscription, usage }
}