# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import threading
import time
import langdetect
import uvicorn

from app.core.config import get_settings
from app.core.db import engine, Base
from app.rag.ingest import ingest

# === Importul Routerelor (Presentation Layer) ===
# Am inclus toate cele 12 module refactorizate pentru a asigura functionalitatea completa
# main.py

# Dacă folderul tău se numește 'routers', folosește:
from app.routers import (
    auth_router as auth,
    account_router as account,
    subscription_router,
    chat_router as chat,
    admin_router as admin,
    billing_router as billing,
    conversation_router as conversations,
    message_router as messages,
    favorite_router as favorites,
    log_router as logs,
    recommendation_router as recommendations,
    usage_router as usage
)

# === Configurare Aplicatie ===
settings = get_settings()
app = FastAPI(
    title="Smart Librarian API",
    description="Sistem expert de recomandări cărți bazat pe RAG și OpenAI",
    version="2.1"
)

# === Eveniment de Startup: Creare Tabele ===
# Aceasta linie asigura ca tabelele sunt create automat in MySQL la pornirea serverului
@app.on_event("startup")
def on_startup():
    print("[INFO] Initializing database tables in MySQL...")
    Base.metadata.create_all(bind=engine)

# === Preîncărcare profile LangDetect ===
_ = langdetect.detect("Aceasta este o propoziție de test.")
print("[INFO] LangDetect profiles preloaded successfully.")

# === Configurare CORS ===
# Permite comunicarea securizata intre Frontend (ex: React) si Backend
origins = origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Înregistrarea tuturor Routerelor ===
# Fiecare router a fost refactorizat pentru a respecta arhitectura pe 3 layere
app.include_router(auth.router)
app.include_router(account.router)
# backend/main.py
app.include_router(subscription_router.router) 
app.include_router(billing.router)
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(favorites.router)
app.include_router(recommendations.router)
app.include_router(usage.router)
app.include_router(logs.router)
app.include_router(admin.router)

# === Healthcheck & Monitoring ===
@app.get("/health", tags=["System"])
def health_check():
    """Verifică dacă API-ul este activ și conectat la MySQL."""
    return {"status": "active", "database": "connected", "version": "2.1"}

# === Funcție de auto-ingest RAG (Background Task) ===
def auto_ingest(interval: int = 600):
    """
    Monitorizează modificările din summaries.json și rulează procesul de ingest
    pentru a actualiza cunoștințele bibliotecarului în ChromaDB.
    """
    last_mtime = None
    # Calea este relativa la structura de foldere a proiectului tau
    data_path = Path(__file__).parent / "data" / "summaries.json"

    while True:
        try:
            if data_path.exists():
                mtime = data_path.stat().st_mtime
                if last_mtime is None or mtime != last_mtime:
                    print("[INFO] Detected change in summaries.json, updating Vector Store...")
                    ingest()
                    last_mtime = mtime
            else:
                print("[WARN] Data file 'summaries.json' not found. Skipping ingest check.")
        except Exception as e:
            print(f"[ERROR] Auto-ingest failed: {e}")
        time.sleep(interval)

# === Pornire thread background pentru ingest ===
# Ruleaza în paralel cu API-ul pentru a nu bloca cererile utilizatorilor
threading.Thread(target=auto_ingest, daemon=True).start()

if __name__ == "__main__":
    print("🚀 Smart Librarian API is starting on http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)