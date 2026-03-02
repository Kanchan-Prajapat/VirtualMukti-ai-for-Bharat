import { useNavigate, useLocation } from "react-router-dom"
import "../../styles/theme.css"

export default function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  const isDashboard = location.pathname === "/dashboard"
  const isHome = location.pathname === "/"

  const handleLogout = () => {
    localStorage.clear()
    navigate("/")
  }

  return (
    <div className="app-header">
      <div
        className="app-brand"
        onClick={() => navigate("/dashboard")}
      >
        <img src="/Logo.jpeg" alt="VirtualMukti Logo" className="brand-logo" />
        <span className="brand-text">VirtualMukti</span>
      </div>

      <div className="nav-actions">
        {!isDashboard && !isHome && (
          <button
            className="secondary-btn"
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </button>
        )}

        {!isHome && (
          <button
            className="danger-btn"
            onClick={handleLogout}
          >
            Logout
          </button>
        )}
      </div>
    </div>
  )
}