import api from "./client";

export async function createSubscription(planCode) {
  // Trimitem planul ca query parameter conform rutei tale de backend
  const { data } = await api.post(`/subscriptions/create`, null, {
    params: { plan: planCode }
  });
  return data;
}

export async function checkRemaining() {
  const { data } = await api.get("/subscriptions/check");
  return data;
}

export async function consumeAttempt() {
  const { data } = await api.post("/subscriptions/consume");
  return data;
}