import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUsers, deleteUser, updateUser, getActionLogs, createUser } from "@/api/admin";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";

export default function AdminPage() {
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ totalUsers: 0, activeSubs: 0, adminCount: 0 });
  const [activeTab, setActiveTab] = useState("users");
  const [loading, setLoading] = useState(true);

  // --- STATE-URI PENTRU EDITARE ---
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: "", role: "", password: "" });

  // --- STATE-URI PENTRU CREARE ---
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createForm, setCreateForm] = useState({ email: "", name: "", role: "user", password: "" });

  const refreshData = async () => {
    try {
      const [uData, lData] = await Promise.all([getUsers(), getActionLogs()]);
      setUsers(uData);
      setLogs(lData);
      
      setStats({
        totalUsers: uData.length,
        activeSubs: uData.filter(u => u.has_active_plan).length,
        adminCount: uData.filter(u => u.role === 'admin').length
      });
    } catch (err) {
      console.error("Eroare la refresh:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
    // Refresh automat la loguri la fiecare 30 secunde pentru a fi "Live"
    const interval = setInterval(refreshData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleCreate = async () => {
    try {
      await createUser(createForm);
      setShowCreateModal(false);
      setCreateForm({ email: "", name: "", role: "user", password: "" });
      refreshData();
    } catch (err) {
      alert(err.response?.data?.detail || "Eroare la creare utilizator");
    }
  };

  async function handleSave() {
    try {
      await updateUser(editing.id, form);
      setEditing(null);
      refreshData();
    } catch (err) {
      alert("Eroare la salvare: " + (err.response?.data?.detail || err.message));
    }
  }

  async function handleDelete(id) {
    if (window.confirm("🗑️ Ești sigur că vrei să elimini acest utilizator?")) {
      try {
        await deleteUser(id);
        refreshData();
      } catch (err) {
        alert("Eroare la ștergere: " + (err.response?.data?.detail || err.message));
      }
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-gray-100 flex">
      <Sidebar />
      <div className="flex-1 ml-60 overflow-y-auto">
        <Navbar />

        <main className="p-8 space-y-8">
          {/* HEADER */}
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-black text-indigo-400">👑 Admin Dashboard</h1>
            <button 
              onClick={() => setShowCreateModal(true)}
              className="bg-indigo-600 hover:bg-indigo-700 px-6 py-2 rounded-xl font-bold transition shadow-lg shadow-indigo-600/20"
            >
              ➕ Adaugă Utilizator
            </button>
          </div>

          {/* STATS */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard title="Total Utilizatori" value={stats.totalUsers} color="blue" icon="👥" />
            <StatCard title="Administratori" value={stats.adminCount} color="red" icon="🛡️" />
            <StatCard title="Abonamente Active" value={stats.activeSubs} color="green" icon="💳" />
            <StatCard title="Sănătate AI" value="99.9%" color="indigo" icon="🧠" />
          </div>

          {/* TABS */}
          <div className="flex space-x-4 border-b border-slate-800">
            <TabBtn active={activeTab === "users"} onClick={() => setActiveTab("users")} label="Utilizatori" />
            <TabBtn active={activeTab === "logs"} onClick={() => setActiveTab("logs")} label="Audit Logs (Live)" />
          </div>

          {/* TAB CONTENT: USERS */}
          {activeTab === "users" && (
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden shadow-xl animate-in fade-in duration-500">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-800/50 text-slate-400 uppercase text-[10px] tracking-widest">
                  <tr>
                    <th className="p-4">Utilizator</th>
                    <th className="p-4">Rol</th>
                    <th className="p-4">Abonament</th>
                    <th className="p-4 text-right">Acțiuni</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-slate-800/30 transition">
                      <td className="p-4">
                        <div className="font-bold">{u.name || "Fără nume"}</div>
                        <div className="text-xs text-slate-500">{u.email}</div>
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${u.role === 'admin' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'}`}>
                          {u.role.toUpperCase()}
                        </span>
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded-md text-[10px] font-bold ${u.has_active_plan ? 'bg-green-500/10 text-green-400' : 'bg-slate-700/30 text-slate-500'}`}>
                          {u.plan_name || "Niciunul"}
                        </span>
                      </td>
                      <td className="p-4 text-right space-x-2">
                        <button onClick={() => {setEditing(u); setForm({name: u.name, role: u.role, password: ""})}} className="p-2 hover:bg-blue-500/20 rounded-lg transition">✏️</button>
                        <button onClick={() => handleDelete(u.id)} className="p-2 hover:bg-red-500/20 rounded-lg transition">🗑️</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* TAB CONTENT: LOGS (AICI ERA PROBLEMA) */}
          {activeTab === "logs" && (
            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-[11px] h-[500px] overflow-y-auto space-y-1 shadow-inner animate-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-indigo-400 mb-4 sticky top-0 bg-slate-950 py-2 border-b border-slate-800 z-10">System Activity Stream (Live from MySQL)</h3>
              {logs.length === 0 ? (
                <div className="text-slate-600 italic p-4">Nu există loguri înregistrate încă...</div>
              ) : (
                logs.map((log) => (
                  <div key={log.id} className="flex gap-4 p-1.5 border-b border-slate-900/50 hover:bg-slate-900 transition items-center">
                    <span className="text-slate-600 min-w-[70px]">[{new Date(log.created_at).toLocaleTimeString()}]</span>
                    <span className={`font-bold px-1.5 py-0.5 rounded ${log.status === 'ERROR' ? 'bg-red-500/10 text-red-500' : 'text-green-500'}`}>
                      {log.action_type}
                    </span>
                    <span className="text-slate-400 flex-1 truncate">{log.description}</span>
                    <span className="text-slate-700 text-[10px]">{log.endpoint}</span>
                  </div>
                ))
              )}
            </div>
          )}
        </main>
      </div>

      {/* ➕ MODAL CREARE UTILIZATOR */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-950/90 backdrop-blur-md flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl w-full max-w-md shadow-2xl space-y-4 animate-in zoom-in-95 duration-200">
            <h2 className="text-xl font-bold text-indigo-400">Adaugă Utilizator</h2>
            <input placeholder="Email" value={createForm.email} onChange={e => setCreateForm({...createForm, email: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500" />
            <input placeholder="Nume" value={createForm.name} onChange={e => setCreateForm({...createForm, name: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500" />
            <input type="password" placeholder="Parolă" value={createForm.password} onChange={e => setCreateForm({...createForm, password: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500" />
            <select value={createForm.role} onChange={e => setCreateForm({...createForm, role: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500">
                <option value="user">User</option>
                <option value="admin">Admin</option>
            </select>
            <div className="flex gap-2 pt-4">
              <button onClick={() => setShowCreateModal(false)} className="flex-1 p-3 bg-slate-800 rounded-xl hover:bg-slate-700 transition">Anulează</button>
              <button onClick={handleCreate} className="flex-1 p-3 bg-indigo-600 rounded-xl font-bold hover:bg-indigo-500 transition">Creează</button>
            </div>
          </div>
        </div>
      )}

      {/* ✏️ MODAL EDITARE UTILIZATOR */}
      {editing && (
        <div className="fixed inset-0 bg-slate-950/90 backdrop-blur-md flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl w-full max-w-md shadow-2xl space-y-4 animate-in zoom-in-95 duration-200">
            <h2 className="text-xl font-bold text-indigo-400">Editează: {editing.email}</h2>
            <input value={form.name} onChange={e => setForm({...form, name: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500" placeholder="Nume" />
            <select value={form.role} onChange={e => setForm({...form, role: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
            <input type="password" placeholder="Parolă nouă (lasă gol)" value={form.password} onChange={e => setForm({...form, password: e.target.value})} className="w-full bg-slate-800 p-3 rounded-xl border border-slate-700 outline-none focus:border-indigo-500" />
            <div className="flex gap-2 pt-4">
              <button onClick={() => setEditing(null)} className="flex-1 p-3 bg-slate-800 rounded-xl hover:bg-slate-700 transition">Anulează</button>
              <button onClick={handleSave} className="flex-1 p-3 bg-blue-600 rounded-xl font-bold hover:bg-blue-500 transition">Salvează</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// HELPERS
function StatCard({ title, value, color, icon }) {
  const colors = { blue: "text-blue-400", green: "text-green-400", red: "text-red-400", indigo: "text-indigo-400" };
  return (
    <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 hover:scale-105 transition shadow-lg">
      <div className="text-2xl mb-2">{icon}</div>
      <div className="text-xs text-slate-500 uppercase font-black">{title}</div>
      <div className={`text-3xl font-black ${colors[color]}`}>{value}</div>
    </div>
  );
}

function TabBtn({ active, onClick, label }) {
  return (
    <button onClick={onClick} className={`pb-4 px-2 text-sm font-bold transition-all ${active ? 'border-b-2 border-indigo-500 text-indigo-400' : 'text-slate-500 hover:text-slate-300'}`}>
      {label}
    </button>
  );
}