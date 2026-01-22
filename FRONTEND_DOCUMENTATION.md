# 📚 Documentația Frontend - Gogu Bibliotecarul

## Cuprins
1. [Introducere](#introducere)
2. [Arhitectura Proiectului](#arhitectura-proiectului)
3. [Instalare și Setup](#instalare-și-setup)
4. [Dependențe](#dependențe)
5. [Structura Fișierelor](#structura-fișierelor)
6. [Componente](#componente)
7. [Pagini (Pages)](#pagini-pages)
8. [API și Integrări](#api-și-integrări)
9. [Autentificare și Autorizare](#autentificare-și-autorizare)
10. [State Management](#state-management)
11. [Styling și Tailwind CSS](#styling-și-tailwind-css)
12. [Fluxul de Date](#fluxul-de-date)
13. [Rute și Navigare](#rute-și-navigare)
14. [Variabile de Mediu](#variabile-de-mediu)
15. [Ghid de Dezvoltare](#ghid-de-dezvoltare)

---

## Introducere

**Gogu Bibliotecarul** este o aplicație web modernă construită cu **React** și **Vite**, care oferă utilizatorilor un asistent AI pentru recomandări de cărți. Aplicația include:

- ✅ **Sistem de autentificare** complet (login, register, forgot password, reset password)
- ✅ **Chat AI** inteligent cu story de carte
- ✅ **Gestionare abonamente** cu suport plăți Stripe
- ✅ **Panou admin** pentru gestionarea utilizatorilor
- ✅ **Responsiv design** cu Tailwind CSS

---

## Arhitectura Proiectului

Frontend-ul folosește o arhitectură modulară cu separare clară a responsabilităților:

```
Frontend (Vite + React 19)
    ├── Routing Layer (React Router v7)
    ├── Authentication Layer (Context API)
    ├── API Layer (Axios + Interceptors)
    ├── UI Components (Tailwind CSS)
    ├── Pages (Feature-based structure)
    └── State Management (Context + Local Storage)
```

### Stack Tehnologic Principal:
- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.2
- **Routing**: React Router DOM 7.8.0
- **HTTP Client**: Axios 1.11.0
- **CSS Framework**: Tailwind CSS 3.3.5
- **Icons**: Lucide React 0.539.0

---

## Instalare și Setup

### Cerințe:
- Node.js 16+ (recomandă 18+)
- npm sau yarn

### Pași de instalare:

```bash
# 1. Navigare în directorul frontend
cd frontend

# 2. Instalare dependențe
npm install

# 3. Configurare variabile de mediu (.env.local)
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env.local

# 4. Pornire server de dezvoltare
npm run dev

# 5. Build producție
npm run build

# 6. Preview build
npm run preview
```

### Verificare setup:
```bash
# Lint cod
npm run lint
```

---

## Dependențe

### Dependențe Principale:

| Pachet | Versiune | Scop |
|--------|----------|------|
| `react` | ^19.1.1 | Framework UI |
| `react-dom` | ^19.1.1 | Render React în DOM |
| `react-router-dom` | ^7.8.0 | Routing și navigare |
| `axios` | ^1.11.0 | HTTP client cu interceptors |
| `tailwindcss` | ^3.3.5 | Utility-first CSS framework |
| `lucide-react` | ^0.539.0 | Icon library |
| `clsx` | ^2.1.1 | Conditional className helper |

### Dependențe de Dezvoltare:

| Pachet | Versiune | Scop |
|--------|----------|------|
| `@vitejs/plugin-react` | ^5.0.0 | HMR pentru React |
| `vite` | ^7.1.2 | Build tool și dev server |
| `eslint` | ^9.33.0 | Code linting |
| `tailwindcss` | ^3.3.5 | CSS compilation |
| `postcss` | ^8.5.6 | CSS transformations |
| `autoprefixer` | ^10.4.21 | Vendor prefixes |

---

## Structura Fișierelor

```
frontend/
├── public/                      # Fișiere statice
│   └── icons/                   # Icon assets
│
├── src/
│   ├── main.jsx                 # Entry point (render React în #root)
│   ├── App.jsx                  # Router principal și layout
│   ├── App.css                  # Stiluri globale component
│   ├── index.css                # Stiluri globale aplicație
│   │
│   ├── api/                     # API integration layer
│   │   ├── client.js            # Axios instance cu interceptors
│   │   ├── auth.js              # Auth endpoints (login, register)
│   │   ├── account.js           # Account endpoints (profile, change password)
│   │   ├── chat.js              # Chat endpoints (sendChat)
│   │   ├── subscription.js      # Subscription endpoints (plans, billing)
│   │   └── admin.js             # Admin endpoints (users, logs)
│   │
│   ├── auth/                    # Authentication context
│   │   ├── authContext.jsx      # Global auth state (AuthProvider)
│   │   └── ProtectedRoute.jsx   # Route guard component
│   │
│   ├── components/              # Reusable UI components
│   │   ├── Navbar.jsx           # Top navigation bar
│   │   ├── Sidebar.jsx          # Side navigation menu
│   │   ├── ChatMessage.jsx      # Single chat message
│   │   ├── MessageInput.jsx     # Input field pentru mesaje
│   │   └── PaymentForm.jsx      # Stripe payment form
│   │
│   ├── lib/                     # Utility libraries
│   │   ├── api.js               # Axios instance definition
│   │   └── auth.js              # Auth helper functions
│   │
│   ├── pages/                   # Page components (full-page views)
│   │   ├── Login.jsx            # Login page
│   │   ├── Register.jsx         # Registration page
│   │   ├── ForgotPassword.jsx   # Forgot password page
│   │   ├── ResetPassword.jsx    # Password reset page
│   │   ├── Chat.jsx             # Main chat interface
│   │   ├── Plans.jsx            # Subscription plans
│   │   ├── Account.jsx          # User account settings
│   │   └── AdminPage.jsx        # Admin dashboard
│   │
│   └── store/                   # State management
│       └── chatStore.js         # (Empty) Chat state store
│
├── index.html                   # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── eslint.config.js            # ESLint configuration
├── jsconfig.json               # JS path aliases
├── package.json                # Dependencies
└── .gitignore                  # Git ignore rules
```

---

## Componente

### 1. **Navbar.jsx** - Bară de navigare superioară

**Locație**: `src/components/Navbar.jsx`

**Scop**: Afișează informații despre utilizator și planul activ

**Caracteristici**:
- Logout button
- Informații plan activ (status, mesaje folosite)
- Logo și branding
- Responsive design

**Props**: Niciun prop direct (folosește `useAuth()` hook)

**State**:
```javascript
const [planInfo, setPlanInfo] = useState(null); // Plan info din backend
```

**Dependințe**:
- `useAuth()` - Auth context
- `fetchOverview()` - API call

**Exemplu utilizare**:
```jsx
import Navbar from "@/components/Navbar";

function App() {
  return <Navbar />;
}
```

---

### 2. **Sidebar.jsx** - Meniu lateral

**Locație**: `src/components/Sidebar.jsx`

**Scop**: Navigare și management cont utilizator

**Caracteristici**:
- Meniu navigare (Chat, Account, Plans)
- Admin panel link (dacă user este admin)
- Logout functionality
- Active route highlighting

**Props**: Niciun prop

**State**: Niciun state local (folosește React Router)

**Dependințe**:
- `useAuth()` - Get user info
- `useLocation()` - Get current route
- `useNavigate()` - Navigate

**Exemplu utilizare**:
```jsx
<div className="flex">
  <Sidebar />
  <main className="flex-1">Content</main>
</div>
```

---

### 3. **ChatMessage.jsx** - Mesaj chat individual

**Locație**: `src/components/ChatMessage.jsx`

**Scop**: Afișare mesaj de utilizator sau asistent

**Props**:
```javascript
{
  role: "user" | "assistant",  // Cine a trimis mesajul
  content: string              // Text mesaj
}
```

**Styling**:
- User messages: gradient cyan-fuchsia, right-aligned
- Assistant messages: white/10 background, left-aligned

**Exemplu utilizare**:
```jsx
<ChatMessage role="user" content="Recomandă-mi o carte" />
<ChatMessage role="assistant" content="Cum e genul tău preferat?" />
```

---

### 4. **MessageInput.jsx** - Input pentru mesaje

**Locație**: `src/components/MessageInput.jsx`

**Scop**: Input field cu validări și constraint management

**Props**:
```javascript
{
  onSend: (message: string) => void,  // Callback trimis mesaj
  disabled: boolean                   // Disable input
}
```

**State**:
```javascript
const [value, setValue] = useState("");      // Text input
const [locked, setLocked] = useState(false); // Locked dacă plan expirat
```

**Funcționalități**:
- Enter key pentru trimis
- Verificare limită abonament (checkRemaining())
- Lockout vizual dacă limită atinsă

**Exemplu utilizare**:
```jsx
<MessageInput 
  onSend={(msg) => console.log(msg)} 
  disabled={false} 
/>
```

---

### 5. **PaymentForm.jsx** - Form plată Stripe

**Locație**: `src/components/PaymentForm.jsx`

**Scop**: Integrare Stripe pentru plăți online

**Props**:
```javascript
{
  planCode: string,     // Codul planului (FREE, STANDARD, PREMIUM)
  onSuccess: () => void, // Callback după succes
  onError: (err) => void // Callback după eroare
}
```

**Dependințe**: Stripe integration

---

## Pagini (Pages)

### 1. **Login.jsx** - Pagina de login

**Locație**: `src/pages/Login.jsx`

**Rută**: `/login`

**Scop**: Autentificare utilizator

**State**:
```javascript
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [err, setErr] = useState(null);
const [loading, setLoading] = useState(false);
```

**Fluxul**:
1. User introduce email și parolă
2. Click "Sign in"
3. API call `login(email, password)`
4. Succes → redirect la `/chat`
5. Eroare → afișare mesaj eroare

**Protecții**:
- Redirect automat la `/chat` dacă user deja logat
- Validări input
- Error handling

---

### 2. **Register.jsx** - Pagina de înregistrare

**Locație**: `src/pages/Register.jsx`

**Rută**: `/register`

**Scop**: Creare cont nou

**State**:
```javascript
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [name, setName] = useState("");
const [confirmPassword, setConfirmPassword] = useState("");
const [error, setError] = useState("");
const [loading, setLoading] = useState(false);
```

**Validări**:
- Email valid
- Parola > 8 caractere
- Parolă == Confirmă parolă
- Nume necesar

**Fluxul**:
1. Validare form
2. API call `register({ email, password, name })`
3. Succes → redirect la `/login`
4. Eroare → afișare mesaj

---

### 3. **ForgotPassword.jsx** - Resetare parolă (Step 1)

**Locație**: `src/pages/ForgotPassword.jsx`

**Rută**: `/forgot-password`

**Scop**: Request reset parolă

**State**:
```javascript
const [email, setEmail] = useState("");
const [submitted, setSubmitted] = useState(false);
const [error, setError] = useState("");
```

**Fluxul**:
1. User introduce email
2. API call `requestPasswordReset(email)`
3. Email cu link reset trimis la user
4. Confirmation message

---

### 4. **ResetPassword.jsx** - Resetare parolă (Step 2)

**Locație**: `src/pages/ResetPassword.jsx`

**Rută**: `/reset-password?token=xyz`

**Scop**: Completare resetare parolă cu token

**State**:
```javascript
const [password, setPassword] = useState("");
const [confirmPassword, setConfirmPassword] = useState("");
const [error, setError] = useState("");
const [success, setSuccess] = useState(false);
```

**Fluxul**:
1. Extract token din URL query params
2. User introduce parolă nouă
3. API call `resetPassword(token, newPassword)`
4. Succes → redirect la `/login`

---

### 5. **Chat.jsx** - Pagina principală de chat

**Locație**: `src/pages/Chat.jsx`

**Rută**: `/chat` (Protected)

**Scop**: Chat cu AI pentru recomandări de cărți

**State**:
```javascript
const [convId, setConvId] = useState(localStorage.getItem("convId"));
const [msgs, setMsgs] = useState([
  { role: "assistant", content: "Salut! Spune-mi ce carte cauți astăzi? 📚✨" }
]);
const [loading, setLoading] = useState(false);
const [locked, setLocked] = useState(false);
```

**Fluxul**:
1. User trimite mesaj via `MessageInput`
2. Verificare limită abonament (`checkRemaining()`)
3. Consum încercare (`consumeAttempt()`)
4. API call `sendChat({ message, conversationId })`
5. Afișare răspuns AI
6. Salvare conversation ID

**Auto-scroll**: La fiecare nou mesaj, scroll automat la sfârşit

**Lockout**: Dacă limita e atinsă, chat se lockează cu mesaj

**Dependințe**:
- `sendChat()` - Send message to AI
- `checkRemaining()` - Verify remaining attempts
- `consumeAttempt()` - Consume one attempt
- `ChatMessage` - Message display
- `MessageInput` - Message input

---

### 6. **Plans.jsx** - Pagina de abonamente

**Locație**: `src/pages/Plans.jsx`

**Rută**: `/plans` (Protected)

**Scop**: Afișare și selecție planuri de abonament

**State**:
```javascript
const [plans, setPlan] = useState([
  { id: 1, code: "FREE", name: "Free", price_cents: 0, ... },
  { id: 2, code: "STANDARD", name: "Standard", price_cents: 499, ... },
  { id: 3, code: "PREMIUM", name: "Premium", price_cents: 1499, ... }
]);
const [selectedPlan, setSelectedPlan] = useState(null);
const [message, setMessage] = useState({ text: "", isError: false });
```

**Planuri disponibile**:

| Plan | Preț | Mesaje/Lună | Caracteristici |
|------|------|-------------|-----------------|
| FREE | €0 | 5 | Acces bază date, răspuns standard |
| STANDARD | €4.99 | 100 | Prioritate AI, istoric salvat |
| PREMIUM | €14.99 | Nelimitat | Ultra-personalizat, suport 24/7 |

**Fluxul**:
1. Afișare 3 plan cards
2. Click "Activează" pe plan
3. FREE → Direct activation (`createSubscription("FREE")`)
4. PAID → Afișare PaymentForm
5. Succes → Update user subscription

**Dependințe**:
- `createSubscription()` - Activate plan
- `PaymentForm` - Stripe integration

---

### 7. **Account.jsx** - Pagina de cont utilizator

**Locație**: `src/pages/Account.jsx`

**Rută**: `/account` (Protected)

**Scop**: Gestionare profil și setări cont

**State**:
```javascript
const [profile, setProfile] = useState(null);           // User profile data
const [overview, setOverview] = useState(null);         // Plan + usage info
const [oldPass, setOldPass] = useState("");             // Current password
const [newPass, setNewPass] = useState("");             // New password
const [saving, setSaving] = useState(false);            // Loading state
const [msg, setMsg] = useState("");                     // Feedback message
```

**Secțiuni**:

#### a) **Profil Informații**
- Nume utilizator
- Email (read-only)
- Data creării contului

#### b) **Plan Activ**
- Status abonament (activ/inactiv)
- Tip plan (FREE, STANDARD, PREMIUM)
- Mesaje folosite / Limită

#### c) **Schimbare Parolă**
```javascript
const onChangePassword = async (e) => {
  e.preventDefault();
  setSaving(true);
  try {
    await changePassword(oldPass, newPass);
    setMsg("✅ Parola a fost schimbată cu succes.");
    setOldPass("");
    setNewPass("");
  } catch (err) {
    setMsg(err.response?.data?.detail || "❌ Eroare la schimbarea parolei.");
  }
};
```

**Calculare Statistici**:
```javascript
const stats = (() => {
  if (!overview?.subscription) return { used: 0, limit: 5, percent: 0 };
  const used = overview.subscription.messages_used || 0;
  const limit = overview.subscription.messages_limit;
  const percent = Math.min((used / limit) * 100, 100);
  return { used, limit, percent, isNearLimit: percent >= 80 };
})();
```

**Dependințe**:
- `fetchProfile()` - Get user info
- `fetchOverview()` - Get plan + usage
- `changePassword()` - Update password

---

### 8. **AdminPage.jsx** - Panou de administrare

**Locație**: `src/pages/AdminPage.jsx`

**Rută**: `/admin` (Protected + Admin role)

**Scop**: Gestionare utilizatori, abonamente, logs

**State**:
```javascript
const [users, setUsers] = useState([]);
const [logs, setLogs] = useState([]);
const [stats, setStats] = useState({ 
  totalUsers: 0, 
  activeSubs: 0, 
  adminCount: 0 
});
const [activeTab, setActiveTab] = useState("users");
const [loading, setLoading] = useState(true);

// Edit/Create state
const [editing, setEditing] = useState(null);
const [form, setForm] = useState({ name: "", role: "", password: "" });
const [showCreateModal, setShowCreateModal] = useState(false);
const [createForm, setCreateForm] = useState({ 
  email: "", name: "", role: "user", password: "" 
});
```

#### a) **Stat Cards**
```jsx
<StatCard title="Total Utilizatori" value={stats.totalUsers} color="blue" icon="👥" />
<StatCard title="Administratori" value={stats.adminCount} color="red" icon="🛡️" />
<StatCard title="Abonamente Active" value={stats.activeSubs} color="green" icon="💳" />
<StatCard title="Sănătate AI" value="99.9%" color="indigo" icon="🧠" />
```

#### b) **Tab: Utilizatori**
Tabel cu coloane:
- Utilizator (Nume + Email)
- Rol (User/Admin badge)
- Abonament (Plan name + status)
- Acțiuni (Edit ✏️, Delete 🗑️)

**Acțiuni**:
- **Edit**: Deschide modal, permite schimbare nume, rol, parolă
- **Delete**: Confirmare, apoi delete din DB

#### c) **Tab: Audit Logs**
Afișare action logs din backend

#### d) **Modal Creare Utilizator**
```jsx
<input placeholder="Email" value={createForm.email} onChange={...} />
<input placeholder="Nume" value={createForm.name} onChange={...} />
<input type="password" placeholder="Parolă" value={createForm.password} onChange={...} />
<select value={createForm.role} onChange={...}>
  <option value="user">User</option>
  <option value="admin">Admin</option>
</select>
```

**Funcții**:

```javascript
const refreshData = async () => {
  const [uData, lData] = await Promise.all([getUsers(), getActionLogs()]);
  setUsers(uData);
  setLogs(lData);
  setStats({
    totalUsers: uData.length,
    activeSubs: uData.filter(u => u.has_active_plan).length,
    adminCount: uData.filter(u => u.role === 'admin').length
  });
};

const handleCreate = async () => {
  await createUser(createForm);
  setShowCreateModal(false);
  refreshData();
};

const handleSave = async () => {
  await updateUser(editing.id, form);
  setEditing(null);
  refreshData();
};

const handleDelete = async (id) => {
  if (window.confirm("Ești sigur?")) {
    await deleteUser(id);
    refreshData();
  }
};
```

**Dependințe**:
- `getUsers()` - Fetch all users
- `getActionLogs()` - Fetch audit logs
- `createUser()` - Create new user
- `updateUser()` - Update user data
- `deleteUser()` - Delete user

---

## API și Integrări

### 1. **API Client Setup** - `src/api/client.js`

Axios instance configurat cu interceptors:

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

// Request Interceptor: Attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response Interceptor: Handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("[Axios] Sesiune expirată");
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

**Caracteristici**:
- ✅ Auto-attach JWT token din localStorage
- ✅ Auto-redirect la /login dacă token expirat (401)
- ✅ Base URL din env vars
- ✅ Error handling centralizat

---

### 2. **Auth API** - `src/api/auth.js`

```javascript
import api from "./client";

export async function register(payload) {
  // payload: { email, password, name, role }
  const { data } = await api.post("/auth/register", payload);
  return data;
}

export async function login(email, password) {
  // Backend expects form-urlencoded (OAuth2)
  const formData = new URLSearchParams();
  formData.append("username", email);  // Email as username
  formData.append("password", password);

  const { data } = await api.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  
  return data; // { access_token, token_type, role }
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
}
```

**Endpoint-uri**:
- `POST /auth/register` - Înregistrare
- `POST /auth/login` - Login (OAuth2 form-urlencoded)
- `GET /auth/me` - Current user info (via AuthContext)

---

### 3. **Account API** - `src/api/account.js`

```javascript
import api from "./client";

export async function fetchProfile() {
  const { data } = await api.get("/account/me");
  return data; // User profile object
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
  return data; // { subscription: {...}, usage: {...} }
}
```

**Endpoint-uri**:
- `GET /account/me` - Profil curent
- `POST /account/change-password` - Schimbare parolă
- `GET /account/overview` - Plan + usage info

---

### 4. **Chat API** - `src/api/chat.js`

```javascript
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
```

**Endpoint-uri**:
- `POST /chat` - Send chat message

**Payload**:
```javascript
{
  message: "Care este cea mai bună carte fantasy?",
  conversation_id: "uuid-optional",
  where: {} // Optional filters
}
```

**Răspuns**:
```javascript
{
  conversation_id: "xyz-123",
  answer: "Recomand 'The Lord of the Rings'...",
  title: "Fantasy Recommendations",
  reason: "Based on your preferences"
}
```

---

### 5. **Subscription API** - `src/api/subscription.js`

```javascript
import api from "./client";

export async function createSubscription(planCode) {
  // planCode: "FREE", "STANDARD", "PREMIUM"
  const { data } = await api.post(`/subscriptions/create`, null, {
    params: { plan: planCode }
  });
  return data;
}

export async function checkRemaining() {
  const { data } = await api.get("/subscriptions/check");
  return data; // { remaining: number, limit: number, ... }
}

export async function consumeAttempt() {
  const { data } = await api.post("/subscriptions/consume");
  return data;
}
```

**Endpoint-uri**:
- `POST /subscriptions/create?plan=FREE` - Activate plan
- `GET /subscriptions/check` - Check remaining attempts
- `POST /subscriptions/consume` - Consume one attempt

---

### 6. **Admin API** - `src/api/admin.js`

```javascript
import api from "./client";

// Users Management
export async function getUsers() {
  const { data } = await api.get("/admin/users");
  return data; // Array of users
}

export async function updateUser(id, payload) {
  // payload: { name, role, password }
  const { data } = await api.put(`/admin/users/${id}`, payload);
  return data;
}

export async function deleteUser(id) {
  await api.delete(`/admin/users/${id}`);
}

export async function createUser(payload) {
  // payload: { email, name, role, password }
  const { data } = await api.post("/admin/users", payload);
  return data;
}

// Plans Management
export async function getPlans() {
  const { data } = await api.get("/admin/plans");
  return data; // Array of plans
}

// Audit Logs
export async function getActionLogs() {
  const { data } = await api.get("/admin/logs");
  return data; // Array of logs
}
```

**Endpoint-uri Admin**:
- `GET /admin/users` - Fetch all users
- `POST /admin/users` - Create user
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/plans` - Fetch plans
- `GET /admin/logs` - Fetch audit logs

---

## Autentificare și Autorizare

### AuthContext - `src/auth/authContext.jsx`

Context global pentru gestionare autentificare și user state.

**State managuat**:
```javascript
const [user, setUser] = useState(null);          // User profile
const [loading, setLoading] = useState(true);    // Loading state
const [plan, setPlan] = useState(null);          // Subscription plan
const [usage, setUsage] = useState(null);        // Usage info
```

**Metode principale**:

#### 1. **login(email, password)**
```javascript
async function login(email, password) {
  try {
    const res = await apiLogin(email, password);
    localStorage.setItem("access_token", res.access_token);
    localStorage.setItem("role", res.role);
    const u = await loadProfile();
    return u.role;
  } catch (err) {
    throw new Error("Login failed");
  }
}
```

#### 2. **logout()**
```javascript
const logout = useCallback(() => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  setUser(null);
  setPlan(null);
  setUsage(null);
  window.location.href = "/login";
}, []);
```

#### 3. **loadProfile()**
```javascript
const loadProfile = useCallback(async () => {
  try {
    const u = await fetchProfile();
    setUser(u);
    await refreshOverview();
    return u;
  } catch (err) {
    setUser(null);
    throw err;
  }
}, []);
```

#### 4. **refresh()**
```javascript
const refresh = useCallback(async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    setLoading(false);
    return;
  }
  try {
    await loadProfile();
  } catch (err) {
    localStorage.removeItem("access_token");
  } finally {
    setLoading(false);
  }
}, [loadProfile]);
```

#### 5. **refreshOverview()**
```javascript
const refreshOverview = useCallback(async () => {
  try {
    const data = await fetchOverview();
    setPlan(data.subscription || null);
    setUsage(data.usage || null);
  } catch (err) {
    setPlan(null);
    setUsage(null);
  }
}, []);
```

**Hook usage**:
```javascript
import { useAuth } from "@/auth/AuthContext";

function MyComponent() {
  const { user, loading, plan, usage, login, logout } = useAuth();
  
  if (loading) return <Spinner />;
  if (!user) return <Redirect to="/login" />;
  
  return <div>Welcome {user.name}</div>;
}
```

---

### ProtectedRoute - `src/auth/ProtectedRoute.jsx`

Component wrapper pentru route protection.

```javascript
export default function ProtectedRoute({ children, requirePlan }) {
  const { user, loading, plan } = useAuth();
  
  if (loading) return <LoadingScreen />;
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  if (requirePlan && !plan) {
    return <Navigate to="/plans" replace />;
  }
  
  return children;
}
```

**Usage**:
```jsx
<Route 
  path="/chat" 
  element={
    <ProtectedRoute requirePlan>
      <ChatPage />
    </ProtectedRoute>
  } 
/>
```

**Props**:
- `children` - Component să rendereze
- `requirePlan` - Check dacă user are plan activ

---

## State Management

### AuthContext (Global State)

State management pentru autentificare este centralizat în `AuthContext`. Alte state-uri sunt locale în componente.

**Flow-ul datelor**:
```
User Login → AuthContext.login() 
  → Save token + role în localStorage 
  → fetchProfile() 
  → Set global user state
  → Redirect la /chat
```

**Local Storage Keys**:
- `access_token` - JWT token pentru API calls
- `role` - User role (user / admin)
- `convId` - Current conversation ID (din Chat page)

**Chat Store** (Empty placeholder):
```javascript
// src/store/chatStore.js - Este gol, nu se folosește actualmente
// Puteti folosi Redux/Zustand dacă apare complexitate mai mare
```

---

## Styling și Tailwind CSS

### Tailwind Config - `tailwind.config.js`

Customization Tailwind cu culori și stiluri brand:

```javascript
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          bg: "#0b0f1a",      // Dark background
          card: "#101729",    // Card background
          text: "#e6eefb",    // Main text
          sub: "#9fb0d1"      // Secondary text
        },
        brand: {
          cyan: "#22d3ee",
          fuchsia: "#d946ef",
          emerald: "#34d399",
          yellow: "#fde047"
        }
      },
      boxShadow: {
        glow: "0 10px 30px rgba(34, 211, 238, 0.25)",     // Cyan glow
        card: "0 10px 30px rgba(2, 6, 23, 0.35)"
      },
      borderRadius: {
        xl2: "1.25rem"
      }
    },
  },
  plugins: [],
};
```

### Culori Brand:
- **Cyan**: `#22d3ee` - Primary accent
- **Fuchsia**: `#d946ef` - Secondary accent
- **Emerald**: `#34d399` - Success color
- **Yellow**: `#fde047` - Warning color

### Clase utile:

| Clasă | Descriere |
|-------|-----------|
| `.shadow-glow` | Cyan glow effect |
| `.shadow-card` | Card shadow effect |
| `.rounded-xl2` | 1.25rem border radius |
| `.bg-slate-950` | Dark background |
| `.text-slate-100` | Light text |

### Exemple styling:

```jsx
// Dark card cu glow effect
<div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl shadow-glow">
  
// Gradient button
<button className="bg-gradient-to-tr from-cyan-400 to-fuchsia-500 px-6 py-2 rounded-xl font-bold">
  
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

---

## Fluxul de Date

### 1. **Fluxul de Autentificare**

```
┌─────────────────────────────────────────────────────────┐
│                    LOGIN FLOW                           │
└─────────────────────────────────────────────────────────┘

1. User → Form (email, password)
2. LoginPage → onClick={onSubmit}
3. onSubmit → api.login(email, password)
4. Backend → Validate + Return access_token + role
5. Frontend → localStorage.setItem(access_token, role)
6. Frontend → AuthContext.loadProfile()
7. Backend → /account/me → Return user data
8. Frontend → Set global user state
9. Frontend → Redirect /chat
```

### 2. **Fluxul de Chat**

```
┌─────────────────────────────────────────────────────────┐
│                     CHAT FLOW                           │
└─────────────────────────────────────────────────────────┘

1. User → Tip mesaj în input
2. onSend() → checkRemaining() → Verify quota
3. ✅ Quota OK → consumeAttempt() → Decrement counter
4. ✅ sendChat({ message, convId })
5. Backend → RAG + AI processing
6. Backend → Return { answer, conversation_id }
7. Frontend → Afișare mesaj în chat
8. Frontend → Save convId în localStorage
```

### 3. **Fluxul de Subscription**

```
┌─────────────────────────────────────────────────────────┐
│              SUBSCRIPTION FLOW                          │
└─────────────────────────────────────────────────────────┘

Plan Selection:
1. User vizitează /plans
2. Click pe plan → setSelectedPlan()

Plan Free:
3. Click "Activează" → handleActivateFree()
4. API call → POST /subscriptions/create?plan=FREE
5. Success → refreshData() → Update UI
6. Plan activate ✅

Plan Paid (STANDARD, PREMIUM):
3. Click "Selectează" → setSelectedPlan()
4. Afișare PaymentForm → Stripe integration
5. Input card details
6. Submit → Stripe API → Backend
7. Backend confirm → Create subscription
8. Success → refreshData()
9. Planul activate ✅
```

### 4. **Fluxul de Admin**

```
┌─────────────────────────────────────────────────────────┐
│              ADMIN MANAGEMENT FLOW                      │
└─────────────────────────────────────────────────────────┘

Load Users:
1. AdminPage → useEffect → refreshData()
2. getUsers() → GET /admin/users
3. getActionLogs() → GET /admin/logs
4. Calculate stats
5. Render table + data

Create User:
6. Click "+ Adaugă Utilizator"
7. Modal → Form input
8. onClick={handleCreate}
9. POST /admin/users → { email, name, role, password }
10. Success → refreshData()
11. User creat ✅

Edit User:
12. Click ✏️ → setEditing(user)
13. Modal cu date pre-filled
14. Modify fields
15. onClick={handleSave}
16. PUT /admin/users/{id} → Updated data
17. Success → refreshData()
18. User updated ✅

Delete User:
19. Click 🗑️
20. Confirmation dialog
21. Confirm → DELETE /admin/users/{id}
22. Success → refreshData()
23. User deleted ✅
```

---

## Rute și Navigare

### React Router Setup - `App.jsx`

```javascript
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          
          {/* Protected User Routes */}
          <Route path="/chat" element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path="/plans" element={<ProtectedRoute><PlansPage /></ProtectedRoute>} />
          <Route path="/account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
          
          {/* Protected Admin Routes */}
          <Route path="/admin" element={<ProtectedRoute><AdminPage /></ProtectedRoute>} />
          
          {/* Redirects */}
          <Route path="/" element={<Navigate to="/chat" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
```

### Rute disponibile:

| Rută | Component | Tip | Descriere |
|------|-----------|-----|-----------|
| `/` | - | Redirect | Redirect la `/chat` |
| `/login` | LoginPage | Public | Login utilizator |
| `/register` | RegisterPage | Public | Înregistrare cont nou |
| `/forgot-password` | ForgotPassword | Public | Request reset parolă |
| `/reset-password` | ResetPassword | Public | Complete reset parolă |
| `/chat` | ChatPage | Protected | Chat cu AI principal |
| `/plans` | PlansPage | Protected | Selectare plan abonament |
| `/account` | AccountPage | Protected | Setări cont utilizator |
| `/admin` | AdminPage | Protected+Admin | Panou administrare |

### Protecție rute:

```javascript
// 1. Dacă nu e logat → redirect /login
<ProtectedRoute>
  <ChatPage />
</ProtectedRoute>

// 2. Dacă nu are plan activ → redirect /plans
<ProtectedRoute requirePlan>
  <ChatPage />
</ProtectedRoute>

// 3. Dacă nu e admin → redirect /chat
<ProtectedRoute requireAdmin>
  <AdminPage />
</ProtectedRoute>
```

### Navigare progamată:

```javascript
import { useNavigate } from "react-router-dom";

function MyComponent() {
  const navigate = useNavigate();
  
  // Navigate la o rută
  navigate("/chat");
  
  // Navigate și replace history
  navigate("/login", { replace: true });
  
  // Navigate cu state
  navigate("/account", { state: { tab: "security" } });
}
```

### Link Component:

```jsx
import { Link } from "react-router-dom";

<Link to="/chat">Go to Chat</Link>
<Link to="/plans" className="btn">Select Plan</Link>
```

---

## Variabile de Mediu

### `.env.local` (Recommended)

```bash
# Backend API URL
VITE_API_BASE_URL=http://127.0.0.1:8000

# Stripe Public Key (dacă se folosește Stripe)
VITE_STRIPE_PUBLIC_KEY=pk_test_xxxxx

# App Mode
VITE_APP_ENV=development
```

### Variabile disponibile:

| Variabilă | Default | Descriere |
|-----------|---------|-----------|
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000` | Backend API URL |
| `VITE_STRIPE_PUBLIC_KEY` | - | Stripe public key |
| `VITE_APP_ENV` | `development` | App environment |

### Accesare în cod:

```javascript
const apiUrl = import.meta.env.VITE_API_BASE_URL;
const stripeKey = import.meta.env.VITE_STRIPE_PUBLIC_KEY;
const env = import.meta.env.VITE_APP_ENV;
```

---

## Ghid de Dezvoltare

### 1. **Setup de Dezvoltare Inițial**

```bash
# 1. Clone repository
git clone <repo-url>
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env.local
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env.local

# 4. Start dev server
npm run dev

# 5. Open browser
# http://localhost:5173
```

### 2. **Creare Component Nou**

**Template**:
```jsx
// src/components/MyComponent.jsx
import { useState, useEffect } from "react";
import { useAuth } from "@/auth/AuthContext";

export default function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    // Initialize
  }, []);

  return (
    <div className="p-4">
      {/* Component content */}
    </div>
  );
}
```

### 3. **Creare Page Nouă**

**Template**:
```jsx
// src/pages/MyPage.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";

export default function MyPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // API call
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">My Page</h1>
      {/* Page content */}
    </div>
  );
}
```

**Apoi add ruta în `App.jsx`**:
```jsx
import MyPage from "@/pages/MyPage";

<Route path="/mypage" element={<ProtectedRoute><MyPage /></ProtectedRoute>} />
```

### 4. **Creare API Module**

**Template** - `src/api/myendpoint.js`:
```javascript
import api from "./client";

export async function fetchMyData(id) {
  const { data } = await api.get(`/myendpoint/${id}`);
  return data;
}

export async function updateMyData(id, payload) {
  const { data } = await api.put(`/myendpoint/${id}`, payload);
  return data;
}

export async function createMyData(payload) {
  const { data } = await api.post(`/myendpoint`, payload);
  return data;
}

export async function deleteMyData(id) {
  await api.delete(`/myendpoint/${id}`);
}
```

**Usage în component**:
```jsx
import { fetchMyData } from "@/api/myendpoint";

useEffect(() => {
  fetchMyData(id)
    .then(data => setData(data))
    .catch(err => console.error(err));
}, [id]);
```

### 5. **Debugging Tips**

#### a) **React DevTools**
Instalează: https://react-devtools-tutorial.vercel.app/

```bash
npm install react-devtools
```

#### b) **Console Logging**
```javascript
console.log("Debug message:", variable);
console.error("Error:", error);
console.warn("Warning:", warning);
```

#### c) **Network Tab (DevTools F12)**
- Monitorizează API calls
- Verifica request/response headers
- Check status codes

#### d) **Local Storage**
```javascript
// Check stored data
localStorage.getItem("access_token");
localStorage.getItem("convId");

// Set test data
localStorage.setItem("test", "value");

// Clear
localStorage.clear();
```

### 6. **Testing API Calls**

Use Postman sau curl:

```bash
# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Test protected endpoint
curl -X GET http://localhost:8000/account/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message", "conversation_id": "optional-id"}'
```

### 7. **Code Style & Linting**

```bash
# Run ESLint
npm run lint

# Fix linting issues
npm run lint -- --fix
```

### 8. **Build pentru Producție**

```bash
# Build optimizat
npm run build

# Output: dist/ folder

# Preview build local
npm run preview

# Deploy dist/ folder la hosting
```

### 9. **Debugging Frecvente**

#### Problem: "Cannot find module '@/component'"
**Soluție**: Verifica path alias în `vite.config.js`:
```javascript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

#### Problem: "401 Unauthorized pe API calls"
**Soluție**: Check token în localStorage:
```javascript
console.log(localStorage.getItem("access_token"));
// Dacă null → re-login
```

#### Problem: "CORS error"
**Soluție**: Verify backend permite CORS:
```python
# Backend FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Problem: "Component not re-rendering"
**Soluție**: Check dependencies în useEffect:
```javascript
useEffect(() => {
  loadData();
}, [id]); // Include dependencies
```

### 10. **Performance Optimization**

#### Lazy loading pages:
```javascript
import { lazy, Suspense } from "react";

const ChatPage = lazy(() => import("@/pages/Chat"));

<Route path="/chat" element={
  <Suspense fallback={<LoadingScreen />}>
    <ChatPage />
  </Suspense>
} />
```

#### Memoization:
```javascript
import { useMemo, useCallback } from "react";

// Memoize expensive calculations
const stats = useMemo(() => {
  return calculateStats(data);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething();
}, [dep]);
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. **DevTools Error: Cannot resolve alias**
```bash
npm install --save-dev vite
npm run dev
```

#### 2. **Axios interceptor not working**
Verify `api` instance export în `src/api/client.js`:
```javascript
export default api; // ✅ Correct
// export const api; // ❌ Wrong
```

#### 3. **localStorage cleared on refresh**
Check browser privacy settings sau use sessionStorage:
```javascript
sessionStorage.setItem("key", "value");
```

#### 4. **Redirect loop /login → /chat → /login**
Verify redirect logic în ProtectedRoute:
```javascript
if (!user && loading === false) {
  return <Navigate to="/login" />;
}
```

#### 5. **API calls hang or timeout**
Check backend server running:
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## Checklist de Publicare (Deployment)

- [ ] Test toate rutele
- [ ] Verifica .env variables setate corect
- [ ] Run `npm run build` și check dist/ output
- [ ] Test API calls spre backend
- [ ] Verifica error handling
- [ ] Test responsiveness pe mobile
- [ ] Check console pentru erori
- [ ] Verifica localStorage data
- [ ] Test logout/login flow
- [ ] Test subscription flows
- [ ] Build și deploy dist/ la hosting

---

## Resurse Utile

- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [React Router Guide](https://reactrouter.com)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Axios Docs](https://axios-http.com)
- [MDN Web Docs](https://developer.mozilla.org)

---

**Document Version**: 1.0  
**Last Updated**: January 15, 2026  
**Maintainer**: Development Team

---

