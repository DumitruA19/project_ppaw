import { useState } from "react";
import { checkRemaining } from "@/api/subscription";

export default function MessageInput({ onSend, disabled }) {
  const [value, setValue] = useState("");
  const [locked, setLocked] = useState(false);

  async function handleSend() {
    const v = value.trim();
    if (!v || disabled || locked) return;

    try {
      await checkRemaining(); // ✅ verifică dacă userul are încercări rămase
      onSend(v);
      setValue("");
    } catch (e) {
      setLocked(true);
    }
  }

  return (
    <div className="flex gap-2">
      <input
        className={`input flex-1 ${locked ? "opacity-60" : ""}`}
        placeholder={
          locked ? "Limita atinsă. Activează un plan nou." : "Scrie un mesaj…"
        }
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        disabled={disabled || locked}
      />
      <button
        className="btn btn-primary"
        onClick={handleSend}
        disabled={disabled || locked}
      >
        {locked ? "Blocat" : "Trimite"}
      </button>
    </div>
  );
}
