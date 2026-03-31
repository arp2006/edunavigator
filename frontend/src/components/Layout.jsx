import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const items = [
    { to: "/dashboard", label: "Recommendations" },
    { to: "/quiz", label: "Aptitude Quiz" },
    { to: "/chat", label: "AI Career Advisor" },
  ];

  if (isAdmin) {
    items.push({ to: "/admin", label: "Admin Panel" });
  }

  return (
    <div className="ed-layout">
      <aside className="ed-sidebar">
        <div className="ed-brand" onClick={() => navigate("/dashboard")} role="button" tabIndex={0}>
          <div className="ed-logo">EduNavigator</div>
          <div className="ed-sub">Intelligent Career & Course Recommender</div>
        </div>

        <nav className="ed-nav">
          {items.map((it) => (
            <NavLink
              key={it.to}
              to={it.to}
              className={({ isActive }) => (isActive ? "ed-nav-link active" : "ed-nav-link")}
            >
              {it.label}
            </NavLink>
          ))}
        </nav>

        <div className="ed-sidebar-footer">
          <div className="ed-user">
            <div className="ed-user-email">{user?.userId ? `User #${user.userId}` : ""}</div>
            <div className="ed-user-role">{user?.role}</div>
          </div>
          <button
            className="ed-btn ed-btn-ghost"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Logout
          </button>
        </div>
      </aside>

      <div className="ed-main">
        <header className="ed-topbar">
          <h1 className="ed-title">EduNavigator</h1>
          <div className="ed-topbar-meta">
            <span className="ed-pill">{user?.role === "admin" ? "Admin Mode" : "Student Mode"}</span>
          </div>
        </header>

        <section className="ed-content">
          <Outlet />
        </section>
      </div>
    </div>
  );
}

