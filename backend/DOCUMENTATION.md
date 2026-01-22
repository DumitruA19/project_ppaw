# 📚 Smart Librarian Backend - Documentație Completă

## 📖 Cuprins
1. [Prezentare Generală](#prezentare-generală)
2. [Tehnologii Utilizate](#tehnologii-utilizate)
3. [Arhitectura Aplicației](#arhitectura-aplicației)
4. [Structura Folderelor](#structura-folderelor)
5. [Instalare și Configurare](#instalare-și-configurare)
6. [Modele de Date](#modele-de-date)
7. [API Endpoints](#api-endpoints)
8. [Fluxul RAG](#fluxul-rag)
9. [Servicii și Logică de Business](#servicii-și-logică-de-business)
10. [Autentificare și Securitate](#autentificare-și-securitate)
11. [Rulare și Testare](#rulare-și-testare)
12. [Ghid de Troubleshooting](#ghid-de-troubleshooting)

---

## Prezentare Generală

**Smart Librarian** este un sistem expert de recomandări de cărți bazat pe:
- **RAG (Retrieval-Augmented Generation)** - folosește ChromaDB pentru stocare vectori și OpenAI pentru generare de conținut
- **Chat Inteligent** - conversații în timp real cu un chatbot alimentat de IA
- **Gestionare Utilizatori** - sistem complet de autentificare, abonamente și plăți
- **Analitică și Logging** - urmărire detaliată a activităților utilizatorilor

### Cazuri de Utilizare
- ✅ Utilizatorii pot primi recomandări personalizate de cărți
- ✅ Conversații cu un chatbot expert în domeniul cărților
- ✅ Gestionare planuri de abonament și plăți
- ✅ Salvarea și organizarea cărților favorite
- ✅ Analiza utilizării și raportare pentru administratori

---

## Tehnologii Utilizate

| Tehnologie | Descriere | Versiune |
|------------|-----------|---------|
| **FastAPI** | Framework web async pentru API REST | ≥ 0.110.0 |
| **Python** | Limbaj de programare | 3.9+ |
| **MySQL** | Baza de date relațională | 8.0+ |
| **ChromaDB** | Vector store pentru RAG | ≥ 0.5.3 |
| **OpenAI API** | Embeddings și generare text | ≥ 1.30.0 |
| **SQLAlchemy** | ORM Python | ≥ 2.0.0 |
| **JWT (PyJWT)** | Autentificare pe bază de token | ≥ 3.3.0 |
| **Uvicorn** | Server ASGI | ≥ 0.27.0 |
| **Pydantic** | Validare date | ≥ 2.0.0 |

---

## Arhitectura Aplicației

Aplicația urmează **Pattern-ul Stratificat (Layered Architecture)**:

```
┌─────────────────────────────────────┐
│     API Routes (Routers)            │ ← Presentation Layer
│  /auth, /chat, /account, etc.       │
└─────────────────────┬───────────────┘
          ↓
┌─────────────────────────────────────┐
│     Services (Business Logic)       │ ← Business Logic Layer
│  ChatService, AuthService, etc.     │
└─────────────────────┬───────────────┘
          ↓
┌─────────────────────────────────────┐
│  Repositories (Data Access)         │ ← Data Access Layer
│  UserRepository, ChatRepository     │
└─────────────────────┬───────────────┘
          ↓
┌─────────────────────────────────────┐
│  Models & Database                  │ ← Persistence Layer
│  SQL Models, Schemas, MySQL         │
└─────────────────────────────────────┘
```

### Avantajele acestei arhitecturi:
- **Separare responsabilități** - fiecare layer are un scop bine definit
- **Testabilitate** - componente independente, ușor de testat
- **Scalabilitate** - ușor de adăugat noi funcționalități
- **Mentenabilitate** - cod organizat și ușor de înțeles

---

## Structura Folderelor

```
backend/
├── app/                          # Aplicația principală
│   ├── core/                     # Configurări și utilitare core
│   │   ├── config.py            # Variabile de mediu și configurări
│   │   ├── db.py                # Conexiune și sesiune bază de date
│   │   ├── security.py          # JWT și autentificare
│   │   ├── dependencies.py      # Dependințe FastAPI
│   │   ├── guard.py             # Rate limiting și protecție
│   │   ├── openai_client.py     # Integrare OpenAI
│   │   └── bad_words.txt        # Cuvinte filtrate
│   ├── models/                   # Modele de date
│   │   ├── sql_models.py        # SQLAlchemy ORM models
│   │   └── schema.py            # Pydantic schemas (request/response)
│   ├── routers/                  # API endpoints (13 module)
│   │   ├── auth_router.py       # Autentificare și registrare
│   │   ├── account_router.py    # Gestionare profil
│   │   ├── chat_router.py       # Chat endpoint principal
│   │   ├── conversation_router.py # Gestionare conversații
│   │   ├── message_router.py    # Gestionare mesaje
│   │   ├── admin_router.py      # Funcții admin
│   │   ├── subscription_router.py # Gestionare abonamente
│   │   ├── billing_router.py    # Gestionare plăți
│   │   ├── favorite_router.py   # Cărți favorite
│   │   ├── recommendation_router.py # Recomandări
│   │   ├── log_router.py        # Jurnale și audit
│   │   ├── usage_router.py      # Statistici utilizare
│   │   └── user_router.py       # Gestionare utilizatori (admin)
│   ├── services/                 # Logica de business
│   │   ├── auth_service.py      # Servicii autentificare
│   │   ├── chat_service.py      # Servicii chat și RAG
│   │   ├── account_service.py   # Servicii cont utilizator
│   │   ├── conversation_service.py # Managementul conversațiilor
│   │   ├── message_service.py   # Managementul mesajelor
│   │   ├── subscription_service.py # Logica abonamente
│   │   ├── billing_service.py   # Logica plăți
│   │   ├── recommendation_service.py # Generare recomandări
│   │   ├── user_service.py      # Servicii utilizator
│   │   ├── admin_service.py     # Servicii admin
│   │   └── [alte servicii]
│   ├── repository/               # Acces date
│   │   ├── auth_repository.py
│   │   ├── user_repository.py
│   │   ├── chat_repository.py
│   │   ├── conversation_repository.py
│   │   └── [alte repository-uri]
│   ├── rag/                      # Retrieval-Augmented Generation
│   │   ├── ingest.py            # Ingestie rezumate în ChromaDB
│   │   ├── retriever.py         # Căutare semantică
│   │   ├── healthcheck_rag.py   # Verificare stare RAG
│   │   └── chroma_inspect.py    # Inspectare colecție Chroma
│   ├── tools/                    # Utilități speciale
│   │   └── summaries.py         # Acces rapid la rezumate
│   ├── utils/                    # Funcții utilitare
│   │   └── logger.py            # Logging personalizat
│   └── __init__.py
│
├── chroma_store/                 # ChromaDB stocare persistentă
│   ├── chroma.sqlite3           # Baza de date Chroma
│   └── [id-uri colecție]/
│
├── data/                         # Date și resurse
│   ├── summaries.json           # Rezumate cărți pentru RAG
│   └── book_summaries.md        # Documentare rezumate
│
├── main.py                       # Punct de intrare aplicație
├── run.py                        # Script alternativ de rulare
├── seed_plans.py                # Script populate plante de abonament
├── requirements.txt              # Dependințe Python
├── .env                          # Variabile de mediu
├── Dockerfile                    # Containerizare Docker
├── README.md                     # Documentare rapidă
└── backend.md                    # Detalii implementare
```

---

## Instalare și Configurare

### 1. Cerințe Preliminare
- **Python 3.9+** instalat
- **MySQL 8.0+** running
- **OpenAI API Key** (obținut de la https://platform.openai.com)
- **pip** (Python package manager)

### 2. Instalare Dependințe

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurare Variabile de Mediu

Creează fișierul `.env` în folderul `backend/`:

```env
# === DATABASE (MySQL) ===
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=Smart_librarian_users

# === API Keys ===
GROQ_API_KEY=your_openai_api_key_here

# === Authentication ===
JWT_SECRET=your_super_secret_jwt_key_change_in_production
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# === RAG / ChromaDB ===
CHROMA_DIR=./chroma_store
COLLECTION_NAME=books

# === Models ===
EMBED_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini

# === CORS ===
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173
```

### 4. Configurare Bază de Date

```bash
# Pornind aplicația, tabelele se vor crea automat:
python main.py

# Alternativ, população plante:
python seed_plans.py
```

---

## Modele de Date

### Diagrama Entități-Relații

```
┌─────────────┐
│   Users     │
│ (identitate)│
└──────┬──────┘
       │
       ├── 1:N → Conversations
       ├── 1:N → Favorites
       ├── 1:N → Subscriptions
       └── 1:N → Payments

┌──────────────────┐
│  Conversations   │
│  (sesiuni chat)  │
└──────┬───────────┘
       │
       ├── 1:N → Messages
       └── 1:N → Recommendations

┌──────────────────┐
│  BillingPlan     │
│  (pachete preț)  │
└──────┬───────────┘
       │
       └── 1:N → Subscriptions

┌──────────────────┐
│  Subscription    │
│  (abonamente)    │
└──────┬───────────┘
       │
       └── 1:N → Payments (istoricul plăților)
```

### Modele SQL

#### **User (Utilizatori)**
```python
{
  "id": "uuid",                    # Identificator unic
  "email": "string",               # Email unic
  "name": "string",                # Numele utilizatorului
  "password_hash": "string",       # Hash bcrypt
  "role": "user|admin",            # Rol utilizator
  "created_at": "datetime"         # Dată creație
}
```

#### **Conversation (Conversații)**
```python
{
  "id": "uuid",                    # Identificator conversație
  "user_id": "uuid",               # FK la User
  "title": "string",               # Titlu conversație
  "created_at": "datetime",        # Dată inițiere
  "updated_at": "datetime"         # Ultima actualizare
}
```

#### **Message (Mesaje)**
```python
{
  "id": "bigint",                  # PK auto-increment
  "conversation_id": "uuid",       # FK la Conversation
  "role": "user|assistant|tool",   # Rol mesaj
  "content": "text",               # Conținut mesaj
  "created_at": "datetime"         # Timp mesaj
}
```

#### **Recommendation (Recomandări)**
```python
{
  "id": "bigint",                  # PK auto-increment
  "conversation_id": "uuid",       # FK la Conversation
  "book_title": "string",          # Titlu carte
  "chroma_doc_id": "string",       # Referință ChromaDB
  "reason": "text",                # Motivația recomandării
  "created_at": "datetime"         # Timp recomandare
}
```

#### **BillingPlan (Planuri Tarife)**
```python
{
  "id": "int",                     # PK auto-increment
  "name": "string",                # Nume plan (free, pro, premium)
  "price_usd": "decimal",          # Preț în USD
  "currency": "string",            # Monedă
  "chat_limit": "int",             # Limite chat/lună
  "description": "text",           # Descriere plan
  "created_at": "datetime"
}
```

#### **Subscription (Abonamente)**
```python
{
  "id": "uuid",                    # PK
  "user_id": "uuid",               # FK la User
  "plan_id": "int",                # FK la BillingPlan
  "status": "active|expired|cancelled", # Status
  "start_date": "date",            # Data inceput
  "end_date": "date",              # Data expirare
  "auto_renew": "boolean",         # Reînnoire automată
  "created_at": "datetime"
}
```

---

## API Endpoints

### 1. **Authentication (`/auth`)**

#### POST `/auth/register`
Înregistrare utilizator nou
```json
Request:
{
  "email": "user@example.com",
  "name": "Ion Popescu",
  "password": "SecurePass123!",
  "role": "user"
}

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Ion Popescu",
  "role": "user",
  "created_at": "2024-01-15T10:30:00",
  "has_active_plan": false,
  "plan_name": "Niciunul"
}
```

#### POST `/auth/login`
Autentificare și obținere JWT token
```json
Request (Form Data):
{
  "username": "user@example.com",  # Email
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/auth/me`
Obținere profil utilizator curent
```json
Request: GET /auth/me
Authorization: Bearer {token}

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Ion Popescu",
  "role": "user",
  "created_at": "2024-01-15T10:30:00",
  "has_active_plan": true,
  "plan_name": "Premium"
}
```

---

### 2. **Chat Principal (`/chat`)**

#### POST `/chat/`
Trimite mesaj și primește recomandări de cărți (endpoint RAG)
```json
Request:
{
  "message": "Vreau o carte de ficțiune științifică pentru ziua copilului",
  "conversation_id": "uuid-optional",
  "history": [
    {"role": "user", "content": "Salut!"},
    {"role": "assistant", "content": "Bună! Sunt Smart Librarian..."}
  ],
  "metadata": {"genre": "sci-fi"},
  "where": {}
}

Response: 200 OK
{
  "id": "uuid-conversație",
  "message_id": 1,
  "response": "Recomand 'Neuromancer' de William Gibson...",
  "recommendations": [
    {
      "title": "Neuromancer",
      "reason": "Opus fondator al cyberpunk...",
      "author": "William Gibson",
      "year": 1984
    }
  ],
  "created_at": "2024-01-15T10:35:00"
}
```

---

### 3. **Conversații (`/conversation`)**

#### GET `/conversation/`
Lista conversații utilizatorului
```json
Response: 200 OK
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Recomandări SF",
    "created_at": "2024-01-15T10:30:00"
  },
  ...
]
```

#### POST `/conversation/`
Crează conversație nouă
```json
Request:
{
  "title": "Recomandări Horror"
}

Response: 201 Created
{
  "id": "uuid-nou",
  "user_id": "uuid",
  "title": "Recomandări Horror",
  "created_at": "2024-01-15T10:30:00"
}
```

#### DELETE `/conversation/{id}`
Șterge conversație și mesajele asociate
```
Response: 204 No Content
```

---

### 4. **Mesaje (`/message`)**

#### GET `/message/conversation/{conversation_id}`
Obții mesajele dintr-o conversație
```json
Response: 200 OK
[
  {
    "id": 1,
    "conversation_id": "uuid",
    "role": "user",
    "content": "Salut!",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "conversation_id": "uuid",
    "role": "assistant",
    "content": "Bună! Cum pot ajuta?",
    "created_at": "2024-01-15T10:30:05"
  }
]
```

---

### 5. **Cărți Favorite (`/favorite`)**

#### POST `/favorite/`
Adaugă carte la favorite
```json
Request:
{
  "book_title": "1984",
  "author": "George Orwell",
  "notes": "Distopic masterpiece"
}

Response: 201 Created
{
  "id": "uuid",
  "user_id": "uuid",
  "book_title": "1984",
  "author": "George Orwell",
  "notes": "Distopic masterpiece",
  "added_at": "2024-01-15T10:30:00"
}
```

#### GET `/favorite/`
Lista cărțile favorite ale utilizatorului
```json
Response: 200 OK
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "book_title": "1984",
    "author": "George Orwell",
    "notes": "Distopic masterpiece",
    "added_at": "2024-01-15T10:30:00"
  }
]
```

#### DELETE `/favorite/{id}`
Șterge carte din favorite
```
Response: 204 No Content
```

---

### 6. **Abonamente (`/subscription`)**

#### GET `/subscription/`
Obții detalii abonament curent
```json
Response: 200 OK
{
  "id": "uuid",
  "user_id": "uuid",
  "plan_id": 2,
  "plan_name": "Premium",
  "status": "active",
  "start_date": "2024-01-01",
  "end_date": "2024-02-01",
  "auto_renew": true,
  "price_usd": 9.99
}
```

#### POST `/subscription/upgrade`
Upgrade la plan superior
```json
Request:
{
  "plan_id": 3
}

Response: 200 OK
{
  "id": "uuid",
  "plan_name": "Premium Plus",
  "status": "active",
  "start_date": "2024-01-15",
  "end_date": "2024-02-15"
}
```

#### POST `/subscription/cancel`
Anulare abonament
```json
Response: 200 OK
{
  "message": "Subscription cancelled successfully",
  "effective_date": "2024-02-01"
}
```

---

### 7. **Plăți (`/billing`)**

#### GET `/billing/plans`
Lista planuri disponibile
```json
Response: 200 OK
[
  {
    "id": 1,
    "name": "Free",
    "price_usd": 0,
    "currency": "USD",
    "chat_limit": 5,
    "description": "Plan gratuit cu limitări"
  },
  {
    "id": 2,
    "name": "Pro",
    "price_usd": 9.99,
    "currency": "USD",
    "chat_limit": 100,
    "description": "Plan profesional"
  }
]
```

#### GET `/billing/invoice/{invoice_id}`
Obții facturi anterioare
```json
Response: 200 OK
{
  "id": "uuid",
  "user_id": "uuid",
  "amount": 9.99,
  "currency": "USD",
  "status": "paid",
  "issued_at": "2024-01-01",
  "due_date": "2024-01-15"
}
```

---

### 8. **Admin (`/admin`)** [Doar pentru role="admin"]

#### GET `/admin/users`
Lista toți utilizatorii
```json
Response: 200 OK
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "name": "Ion Popescu",
    "role": "user",
    "created_at": "2024-01-15T10:30:00",
    "subscription_status": "active"
  }
]
```

#### PATCH `/admin/user/{user_id}/role`
Schimbă rol utilizator
```json
Request:
{
  "role": "admin"
}

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "admin",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### GET `/admin/analytics`
Statistici utilizare
```json
Response: 200 OK
{
  "total_users": 150,
  "active_subscriptions": 45,
  "total_revenue": 4495.50,
  "monthly_growth": 12.5,
  "top_books": ["1984", "Sapiens", "Neuromancer"]
}
```

---

### 9. **Utilizatori (`/user`)** [Admin]

#### GET `/user/`
Lista utilizatori cu detalii complete
```json
Response: 200 OK
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "name": "Ion Popescu",
    "role": "user",
    "created_at": "2024-01-15T10:30:00",
    "last_login": "2024-01-15T15:00:00",
    "subscription": {...},
    "usage": {...}
  }
]
```

---

### 10. **Logs (`/log`)** [Admin]

#### GET `/log/audit`
Jurnal audit complet
```json
Response: 200 OK
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "action": "LOGIN",
    "resource": "auth",
    "status": "success",
    "ip_address": "192.168.1.1",
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

---

### 11. **Utilizare (`/usage`)**

#### GET `/usage/me`
Statistici personale de utilizare
```json
Response: 200 OK
{
  "user_id": "uuid",
  "total_chat_requests": 42,
  "total_recommendations": 128,
  "total_favorites": 15,
  "current_month_usage": 12,
  "plan_limit": 100,
  "usage_percentage": 12.0
}
```

---

### 12. **Recomandări (`/recommendation`)**

#### GET `/recommendation/conversation/{conversation_id}`
Recomandări din conversație
```json
Response: 200 OK
[
  {
    "id": 1,
    "book_title": "Neuromancer",
    "author": "William Gibson",
    "reason": "Opus fondator al cyberpunk...",
    "chroma_doc_id": "doc-123",
    "created_at": "2024-01-15T10:35:00"
  }
]
```

---

### 13. **Cont (`/account`)**

#### GET `/account/profile`
Profil detaliat
```json
Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Ion Popescu",
  "phone": "+40712345678",
  "avatar_url": "https://...",
  "bio": "Iubitor de SF",
  "created_at": "2024-01-15T10:30:00",
  "preferences": {
    "language": "ro",
    "theme": "dark",
    "email_notifications": true
  }
}
```

#### PATCH `/account/profile`
Actualizare profil
```json
Request:
{
  "name": "Ion Pop",
  "phone": "+40712345679",
  "bio": "Iubitor de SF și Horror"
}

Response: 200 OK
{
  "message": "Profile updated successfully",
  "profile": {...}
}
```

#### PATCH `/account/password`
Schimbare parolă
```json
Request:
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!"
}

Response: 200 OK
{
  "message": "Password changed successfully"
}
```

---

## Fluxul RAG

### Ce este RAG?
**RAG (Retrieval-Augmented Generation)** combinează:
1. **Retrieval** - căutare în baza de date vectori (ChromaDB)
2. **Augmentation** - adăugare context din documente găsite
3. **Generation** - generare răspuns de LLM bazat pe context

### Fluxul Complet

```
┌─────────────────────────────────┐
│  1. INGESTIE (Una odată)        │
│  app/rag/ingest.py              │
└──────────────┬──────────────────┘
               │
               ├─→ Citire summaries.json
               ├─→ Creare embeddings cu OpenAI
               └─→ Stocare în ChromaDB
                      ↓
┌─────────────────────────────────┐
│  2. CHAT - Utilizator trimite   │
│  mesaj prin /chat/endpoint      │
└──────────────┬──────────────────┘
               │
               ├─→ Validare JWT (Securitate)
               ├─→ Verificare abonament
               └─→ Salvare mesaj în DB
                      ↓
┌─────────────────────────────────┐
│  3. RETRIEVAL                   │
│  app/rag/retriever.py           │
└──────────────┬──────────────────┘
               │
               ├─→ Embedare întrebării
               ├─→ Căutare în ChromaDB
               └─→ Extragere top N rezultate
                      ↓
┌─────────────────────────────────┐
│  4. AUGMENTATION                │
│  Construire context             │
└──────────────┬──────────────────┘
               │
               ├─→ Citire rezumate
               ├─→ Formatare context
               └─→ Construire prompt
                      ↓
┌─────────────────────────────────┐
│  5. GENERATION                  │
│  ChatGPT API                    │
└──────────────┬──────────────────┘
               │
               ├─→ Trimitere prompt augmentat
               ├─→ Primire răspuns cu IA
               └─→ Salvare răspuns în DB
                      ↓
┌─────────────────────────────────┐
│  6. RĂSPUNS UTILIZATOR          │
│  Feedback complet cu recomandări│
└─────────────────────────────────┘
```

### Implementare Tehnică

#### a) **Ingestie (seed_rag.py)**
```python
# Citire summaries.json
summaries = json.load(open('data/summaries.json'))

# Pentru fiecare carte:
for book in summaries:
    # 1. Creare embedding
    embedding = openai.Embedding.create(
        input=book['summary'],
        model="text-embedding-3-small"
    )
    
    # 2. Adaugare în ChromaDB
    collection.add(
        ids=[book['id']],
        embeddings=[embedding['data'][0]['embedding']],
        metadatas=[{
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre']
        }],
        documents=[book['summary']]
    )
```

#### b) **Retrieval (retriever.py)**
```python
# Utilizator trimite întrebare
user_query = "Vreau o carte de SF"

# 1. Embedare întrebare
query_embedding = openai.Embedding.create(
    input=user_query,
    model="text-embedding-3-small"
)['data'][0]['embedding']

# 2. Căutare în ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,  # Top 3 cărți relevante
    where={"genre": {"$eq": "sci-fi"}}  # Filtru opțional
)

# 3. Extragere informații
recommended_books = [{
    'title': metadata['title'],
    'summary': document,
    'relevance': distance
} for metadata, document, distance in results]
```

#### c) **Augmentation & Generation**
```python
# Construire prompt cu context
augmented_prompt = f"""
Tu ești bibliotecarul inteligent Smart Librarian.
Pe baza următoarelor cărți și rezumatelor lor:

{format_retrieved_books(recommended_books)}

Răspunde la întrebarea utilizatorului:
"{user_query}"

Oferă recomandări personalizate cu explicații.
"""

# Trimitere la ChatGPT
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Ești Smart Librarian..."},
        {"role": "user", "content": augmented_prompt}
    ]
)
```

---

## Servicii și Logică de Business

### 1. **ChatService** (`app/services/chat_service.py`)

Gestionează întreaga logică de chat și RAG.

**Metodă principală**: `process_chat(user, request)`
```python
def process_chat(self, user: User, request: ChatRequest) -> ChatResponse:
    # 1. Validare abonament
    if not user.has_active_plan:
        raise ValueError("Abonament necesar pentru chat")
    
    # 2. Verificare limită utilizare
    usage = self.usage_repo.get_monthly_usage(user.id)
    if usage.exceeds_plan_limit():
        raise ValueError("Limită lunară atinsă")
    
    # 3. Creare/obținere conversație
    conv = self._get_or_create_conversation(user, request)
    
    # 4. Salvare mesaj utilizator
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=request.message
    )
    self.db.add(user_msg)
    
    # 5. RAG: Căutare și augmentare
    retrieved_books = self.retriever.search(
        query=request.message,
        where=request.metadata
    )
    
    # 6. Generare răspuns cu OpenAI
    response_text = self.openai_client.generate_chat(
        messages=request.history,
        context=retrieved_books
    )
    
    # 7. Salvare răspuns
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=response_text
    )
    self.db.add(assistant_msg)
    
    # 8. Salvare recomandări
    for book in retrieved_books:
        rec = Recommendation(
            conversation_id=conv.id,
            book_title=book.title,
            reason=self._generate_reason(book)
        )
        self.db.add(rec)
    
    # 9. Actualizare statistici
    self.usage_repo.increment_monthly_usage(user.id)
    
    self.db.commit()
    return ChatResponse(...)
```

### 2. **AuthService** (`app/services/auth_service.py`)

Gestionează înregistrare, login și validare.

```python
class AuthService:
    def register(self, email: str, name: str, password: str, role: str = "user"):
        # 1. Validare email unic
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already registered")
        
        # 2. Hash parolă
        password_hash = get_password_hash(password)
        
        # 3. Creare utilizator
        user = User(
            email=email,
            name=name,
            password_hash=password_hash,
            role=role
        )
        self.db.add(user)
        
        # 4. Alocare plan gratuit implicit
        free_plan = self.subscription_repo.get_plan_by_name("Free")
        subscription = Subscription(
            user_id=user.id,
            plan_id=free_plan.id,
            status="active"
        )
        self.db.add(subscription)
        
        self.db.commit()
        return user
    
    def login(self, email: str, password: str):
        # 1. Obținere utilizator
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Credențiale invalide")
        
        # 2. Verificare parolă
        if not verify_password(password, user.password_hash):
            raise ValueError("Credențiale invalide")
        
        # 3. Generare JWT token
        token = create_access_token(user.id)
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }
```

### 3. **SubscriptionService** (`app/services/subscription_service.py`)

Gestionează abonamente și upgrade-uri.

```python
class SubscriptionService:
    def upgrade_subscription(self, user_id: str, plan_id: int):
        # 1. Obținere abonament curent
        current_sub = self.subscription_repo.get_active_by_user(user_id)
        
        # 2. Validare plan nou
        new_plan = self.billing_repo.get_plan(plan_id)
        if new_plan.price < current_sub.plan.price:
            raise ValueError("Nu poți downgrade-ui abonamentul")
        
        # 3. Procesare plată (dacă paid)
        if new_plan.price > 0:
            self._process_payment(user_id, new_plan)
        
        # 4. Actualizare abonament
        current_sub.plan_id = plan_id
        current_sub.start_date = date.today()
        current_sub.end_date = date.today() + timedelta(days=30)
        
        self.db.commit()
        return current_sub
```

### 4. **RecommendationService** (`app/services/recommendation_service.py`)

Generează recomandări personalizate.

```python
class RecommendationService:
    def generate_recommendations(self, conversation_id: str):
        # 1. Obținere ultimele mesaje
        messages = self.message_repo.get_recent(conversation_id, limit=5)
        
        # 2. Analiză context
        context = self._analyze_conversation_context(messages)
        
        # 3. Căutare semantică
        retrieved = self.retriever.search(
            query=context.get('theme', ''),
            where=context.get('filters', {})
        )
        
        # 4. Rancare recomandări
        ranked = self._rank_recommendations(retrieved, context)
        
        return ranked[:5]  # Top 5
```

---

## Autentificare și Securitate

### 1. **JWT Authentication**

```python
# app/core/security.py

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    """Creează JWT token"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Validează token și returnează utilizator"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Token invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
    
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Utilizator nu găsit")
    
    return user
```

### 2. **Password Hashing**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash parolă cu bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifică parolă"""
    return pwd_context.verify(plain_password, hashed_password)
```

### 3. **CORS Configuration**

```python
# main.py

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. **Rate Limiting** (`app/core/guard.py`)

Protejează endpoint-urile de abuz.

```python
class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window  # secunde
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Șterge cereri vechi
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.time_window
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True
```

### 5. **Validare Input**

```python
# app/core/guard.py

def sanitize_input(text: str) -> str:
    """Elimină conținut malițios"""
    # Elimină HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Verifică cuvinte interzise
    bad_words = load_bad_words()
    for word in bad_words:
        text = text.replace(word, "*" * len(word))
    
    # Limitează lungime
    return text[:5000]
```

---

## Rulare și Testare

### 1. **Pornire Server**

```bash
# Instalare dependințe
pip install -r requirements.txt

# Verificare .env
cat .env

# Inițializare ChromaDB (eerste data)
python -m app.rag.ingest

# Pornire server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. **Rulare în Docker**

```bash
# Build image
docker build -t smart-librarian-backend .

# Run container
docker run -p 8000:8000 --env-file .env smart-librarian-backend

# Sau cu docker-compose
docker-compose up backend
```

### 3. **Testare API**

#### Cu cURL:
```bash
# Înregistrare
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "TestPass123!",
    "role": "user"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=TestPass123!"

# Chat
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "message": "Recomandă-mi o carte de SF",
    "history": []
  }'
```

#### Cu Postman:
1. Deschide Postman
2. Importă colecția din `postman_collection.json` (dacă există)
3. Testează fiecare endpoint

#### Cu pytest:
```bash
# Rulare teste
pytest tests/ -v

# Rulare cu coverage
pytest tests/ --cov=app --cov-report=html
```

### 4. **Exemple de Testare**

```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "name": "Test",
        "password": "TestPass123!",
        "role": "user"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"

def test_login():
    # Înregistrare mai întâi
    client.post("/auth/register", json={...})
    
    # Login
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_chat():
    token = "valid_jwt_token"
    response = client.post(
        "/chat/",
        json={"message": "Recomandă o carte"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

---

## Ghid de Troubleshooting

### Eroare: "CORS policy: blocked"
**Cauză**: Frontend și backend pe domenii diferite
**Soluție**:
```python
# Actualizează .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Sau în config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### Eroare: "Can't connect to MySQL"
```bash
# Verifică dacă MySQL rulează
mysql --version

# Testează conexiunea
mysql -u root -p -h localhost

# Verifică .env
echo $MYSQL_HOST
echo $MYSQL_PORT

# Resetează conexiune
sudo service mysql restart  # Linux
mysql.server restart        # macOS
```

### Eroare: "OpenAI API key invalid"
```bash
# Verifică cheia
echo $GROQ_API_KEY

# Generează nouă cheie de la https://platform.openai.com/api-keys
# Actualizează .env
```

### Eroare: "ChromaDB collection empty"
```python
# Reîncarcă colecția
python -m app.rag.ingest

# Verifică colecția
python -m app.rag.chroma_inspect
```

### Performanță Lentă
1. **Indexare bază de date**: `CREATE INDEX idx_user_email ON users(email);`
2. **Caching**: Implementează Redis
3. **Paginare**: Adaugă `skip` și `limit` la endpoints
4. **Monitorizare**: Instalează `prometheus` și `grafana`

### Debug Mode
```python
# main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Sau cu loguru
from loguru import logger
logger.enable("app")
```

---

## Dosare și Resurse Importante

| Fișier | Scop |
|--------|------|
| `.env` | Variabile de mediu |
| `requirements.txt` | Dependințe Python |
| `main.py` | Punct de intrare |
| `Dockerfile` | Containerizare |
| `docker-compose.yml` | Orchestrare containere |
| `data/summaries.json` | Baza de date cărți |
| `app/core/config.py` | Configurații |
| `app/rag/ingest.py` | Script ingestie RAG |

---

## Contact și Support

Pentru probleme sau întrebări:
- 📧 Email: support@smartlibrarian.ro
- 🐛 Issues: https://github.com/..../issues
- 📖 Documentație completa: https://docs.smartlibrarian.ro

---

## Versiune

- **Versiune API**: 2.1
- **Dată Update**: 15 Ianuarie 2024
- **Status**: Production Ready

---

**Gata! 🎉 Documentația completă a backend-ului Smart Librarian este acum disponibilă.**
