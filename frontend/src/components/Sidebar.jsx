// // src/components/Sidebar.jsx
// import { Link, useLocation, useNavigate } from "react-router-dom";
// import { logout } from "@/api/auth";
// import { useAuth } from "@/auth/AuthContext";

// export default function Sidebar() {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const { user } = useAuth();

//   const baseMenu = [
//     { label: "Contul meu", path: "/account" },
//     { label: "Planuri", path: "/plans" },
//     { label: "Conversații", path: "/chat" },
//   ];

//   // ✅ Meniu suplimentar pentru admini
//   const adminMenu = [
//     { label: "Panou Admin", path: "/admin" },
//     { label: "👥 Gestionare angajați", path: "/admin/employees" },
//     { label: "💳 Abonamente", path: "/admin/subscriptions" },
//     { label: "➕ Creare utilizator", path: "/admin/create-user" },
//   ];

//   const handleLogout = () => {
//     logout();
//     navigate("/login");
//   };

//   if (!user) return null;

//   const isAdmin = user.role === "admin";

//   return (
//     <aside className="w-60 h-screen fixed bg-gray-900 text-white flex flex-col p-4 border-r border-slate-800">
//       <h2 className="text-xl font-semibold mb-6">📚 Gogu Bibliotecarul</h2>

//       <nav className="flex-1 space-y-2 overflow-y-auto">
//         {baseMenu.map((item) => (
//           <Link
//             key={item.path}
//             to={item.path}
//             className={`block px-3 py-2 rounded hover:bg-gray-700 ${
//               location.pathname === item.path ? "bg-gray-700" : ""
//             }`}
//           >
//             {item.label}
//           </Link>
//         ))}

//         {isAdmin && (
//           <>
//             <div className="mt-4 mb-2 text-gray-400 uppercase text-xs font-semibold tracking-wide">
//               Admin
//             </div>
//             {adminMenu.map((item) => (
//               <Link
//                 key={item.path}
//                 to={item.path}
//                 className={`block px-3 py-2 rounded hover:bg-gray-700 ${
//                   location.pathname === item.path ? "bg-gray-700" : ""
//                 }`}
//               >
//                 {item.label}
//               </Link>
//             ))}
//           </>
//         )}
//       </nav>

//       <button
//         onClick={handleLogout}
//         className="mt-auto bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
//       >
//         Ieșire
//       </button>
//     </aside>
//   );
// }


// src/components/Sidebar.jsx
import { Link, useLocation, useNavigate } from "react-router-dom";
import { logout } from "@/api/auth";
import { useAuth } from "@/auth/AuthContext";

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

  // 🔒 Dacă nu e logat, nu afișăm sidebarul
  if (!user) return null;

  const isAdmin = user.role === "admin";

  // 🌐 Meniu pentru utilizatori normali
  const userMenu = [
    { label: "🏠 Contul meu", path: "/account" },
    { label: "💼 Planuri", path: "/plans" },
    { label: "💬 Conversații", path: "/chat" },
  ];

  // 👑 Meniu pentru administratori
  const adminMenu = [
    { label: "📊 Panou Admin", path: "/admin" },
    // { label: "👥 Gestionare angajați", path: "/admin/employees" },
    // { label: "💳 Abonamente", path: "/admin/subscriptions" },
    // { label: "➕ Creare utilizator", path: "/admin/create-user" },
  ];

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  // 🧱 Stil comun pentru linkuri
  const linkClass = (path) =>
    `block px-3 py-2 rounded hover:bg-gray-700 transition ${
      location.pathname === path ? "bg-gray-700 text-cyan-300" : ""
    }`;

  return (
    <aside className="w-60 h-screen fixed bg-gray-900 text-white flex flex-col p-4 border-r border-slate-800">
      <h2 className="text-xl font-semibold mb-6">
        📚 Gogu Bibliotecarul
      </h2>

      {/* NAVIGATION */}
      <nav className="flex-1 space-y-2 overflow-y-auto">
        {isAdmin
          ? adminMenu.map((item) => (
              <Link key={item.path} to={item.path} className={linkClass(item.path)}>
                {item.label}
              </Link>
            ))
          : userMenu.map((item) => (
              <Link key={item.path} to={item.path} className={linkClass(item.path)}>
                {item.label}
              </Link>
            ))}
      </nav>

      {/* LOGOUT BUTTON */}
      <button
        onClick={handleLogout}
        className="mt-auto bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded font-semibold transition"
      >
        Ieșire
      </button>
    </aside>
  );
}
