import api from "./client";

export async function sendChat({ message, conversationId, where = {} }) {
  if (!message?.trim()) throw new Error("Mesajul nu poate fi gol.");

  const payload = {
    message,
    ...(conversationId && { conversation_id: conversationId }),
    where,
  };

  const { data } = await api.post("/chat", payload);
  return data; // { conversation_id, answer, title, reason }
}