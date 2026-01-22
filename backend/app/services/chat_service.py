from sqlalchemy.orm import Session
from app.repository import chat_repository as repo
from app.core.openai_client import chat_complete
from app.services.subscription_service import SubscriptionService
from app.rag import retriever
from app.models import schema as s

SYSTEM_PROMPT = (
    "Ești Smart Librarian, un expert în recomandări de cărți. "
    "Folosește contextul oferit pentru a răspunde. Dacă nu găsești informația, "
    "răspunde politicos că nu știi, dar sugerează ceva similar."
)

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.sub_service = SubscriptionService(db)

    def process_chat(self, user, req: s.ChatRequest) -> s.ChatResponse:
        # 1️⃣ Verifică limitele abonamentului
        if not self.sub_service.can_use_feature(str(user.id)):
            raise ValueError("Ai atins limita de mesaje pentru planul tău actual.")

        # 2️⃣ Conversație existentă sau nouă
        conv = repo.get_conversation(self.db, str(req.conversation_id)) if req.conversation_id else None
        if not conv:
            conv = repo.create_conversation(self.db, str(user.id), title=req.message[:50])

        # 3️⃣ Recuperare context RAG (ChromaDB)
        rag_result = retriever.similar(req.message, k=5)
        context = "\n---\n".join(rag_result["documents"][0]) if rag_result["documents"] else "Fără context suplimentar."

        # 4️⃣ Construire istoric mesaje pentru OpenAI
        history = repo.get_history(self.db, conv.id)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Adăugăm ultimele replici pentru contextul conversației
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Adăugăm mesajul curent împreună cu contextul din cărți
        messages.append({
            "role": "user", 
            "content": f"Context din bibliotecă:\n{context}\n\nÎntrebare: {req.message}"
        })

        # 5️⃣ Apel OpenAI și salvare rezultate
        result = chat_complete(messages)
        answer = result["text"]

        self.sub_service.consume_attempt(str(user.id)) # Scădem din cotă
        repo.add_message(self.db, conv.id, "user", req.message)
        repo.add_message(self.db, conv.id, "assistant", answer)
        
        self.db.commit()

        return s.ChatResponse(conversation_id=conv.id, answer=answer, title=conv.title)
    
    
  

# app/services/chat_service.py
from app.utils.logger import log_event # Asigură-te că ai creat utilitarul anterior

def process_chat(self, user, req: s.ChatRequest) -> s.ChatResponse:
    user_id_str = str(user.id)
    
    # 1. Verifică limitele (MySQL)
    if not self.sub_service.can_use_feature(user_id_str):
        log_event(
            self.db, user.id, "CHAT_LIMIT", "/chat", 
            "Utilizatorul a încercat să trimită un mesaj dar a atins limita planului.", 
            status="WARNING"
        )
        raise ValueError("Ai atins limita de mesaje.")

    # 2. Gestionează conversația (MySQL)
    conv = repo.get_conversation(self.db, str(req.conversation_id)) if req.conversation_id else None
    if not conv:
        conv = repo.create_conversation(self.db, user_id_str, title=req.message[:50])
        log_event(self.db, user.id, "CHAT_NEW_CONV", "/chat", f"Conversație nouă creată: {conv.id}")

    # 3. RAG Context (ChromaDB local)
    try:
        rag_result = retriever.similar(req.message, k=5)
        context = "\n---\n".join(rag_result["documents"][0]) if rag_result["documents"] else "Fără context."
    except Exception as e:
        context = "Eroare la recuperarea contextului."
        log_event(self.db, user.id, "RAG_ERROR", "/chat", f"Eroare ChromaDB: {str(e)}", status="ERROR")

    # 4. Apel AI cu FALLBACK
    try:
        # Aici se face apelul către Groq/OpenAI
        result = chat_complete(messages) 
        answer = result["text"]
        ai_status = "SUCCESS"
    except Exception as e:
        # DACĂ AI-ul dă eroare, punem un răspuns de rezervă
        print(f"[FALLBACK] Eroare AI: {e}")
        answer = "⚠️ Momentan am o problemă tehnică de conectare la AI, dar mesajul tău a fost salvat și contorizat! 📚"
        ai_status = "FALLBACK"
        log_event(self.db, user.id, "AI_ERROR", "/chat", f"Eroare Groq/OpenAI: {str(e)}", status="ERROR")

    # 5. Salvează și contorizează (MySQL)
    try:
        self.sub_service.consume_attempt(user_id_str)
        repo.add_message(self.db, conv.id, "user", req.message)
        repo.add_message(self.db, conv.id, "assistant", answer)
        self.db.commit()

        # Log final pentru succesul operațiunii
        log_event(
            self.db, user.id, "CHAT_COMPLETED", "/chat", 
            f"Mesaj procesat cu succes (Status AI: {ai_status})", 
            status="SUCCESS"
        )
    except Exception as e:
        self.db.rollback()
        log_event(self.db, user.id, "DB_ERROR", "/chat", f"Eroare la salvarea în MySQL: {str(e)}", status="ERROR")
        raise e

    return s.ChatResponse(conversation_id=conv.id, answer=answer, title=conv.title)