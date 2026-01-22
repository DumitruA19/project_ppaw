import React, { useEffect, useRef, useState } from "react";
import { sendChat } from "@/api/chat";
import { checkRemaining, consumeAttempt } from "@/api/subscription";
import ChatMessage from "@/components/ChatMessage";
import MessageInput from "@/components/MessageInput";

export default function ChatPage() {
  const [convId, setConvId] = useState(localStorage.getItem("convId"));
  const [msgs, setMsgs] = useState([
    { role: "assistant", content: "Salut! Spune-mi ce carte cauți astăzi? 📚✨" },
  ]);
  const [loading, setLoading] = useState(false);
  const [locked, setLocked] = useState(false);
  const listRef = useRef(null);

  // Auto-scroll la ultimul mesaj
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [msgs, loading]);

  async function onSend(text) {
    if (!text || locked || loading) return;

    setMsgs((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);

    try {
      // 1. Verificări abonament
      await checkRemaining();
      await consumeAttempt();

      // 2. Comunicare cu AI
      const res = await sendChat({ message: text, conversationId: convId });
      
      if (res.conversation_id !== convId) {
        setConvId(res.conversation_id);
        localStorage.setItem("convId", res.conversation_id);
      }

      setMsgs((prev) => [...prev, { role: "assistant", content: res.answer }]);
    } catch (err) {
      const detail = err.response?.data?.detail || "Eroare la procesarea cererii.";
      setMsgs((prev) => [...prev, { role: "assistant", content: `⚠️ ${detail}` }]);
      
      // Blocăm chat-ul dacă limita a fost atinsă
      if (err.response?.status === 403 || detail.toLowerCase().includes("limit")) {
        setLocked(true);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container py-6 grid gap-4 h-[calc(100vh-80px)] max-w-4xl mx-auto">
      <div ref={listRef} className="bg-slate-900/50 border border-slate-800 rounded-2xl p-4 overflow-y-auto space-y-4 shadow-inner">
        {msgs.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}
        {loading && <ChatMessage role="assistant" content="Se generează răspunsul..." isTyping />}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
        <MessageInput onSend={onSend} disabled={loading || locked} />
        {locked && (
          <div className="text-red-400 text-sm mt-3 text-center bg-red-950/20 py-2 rounded-lg border border-red-500/20">
            Ai atins limita planului tău. <a href="/plans" className="underline font-bold hover:text-red-300">Upgradează acum</a>.
          </div>
        )}
      </div>
    </div>
  );
}