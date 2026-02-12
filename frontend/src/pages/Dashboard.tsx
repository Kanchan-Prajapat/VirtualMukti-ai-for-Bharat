import { useEffect, useState } from "react"
import api from "../config/api"
import { useNavigate } from "react-router-dom"
import "../../styles/theme.css"

export default function Dashboard() {
  const [userInfo, setUserInfo] = useState<any>(null)
  const [prediction, setPrediction] = useState<any>(null)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const [userRes, predRes] = await Promise.all([
        api.get("/api/auth/me"),
        api.get("/api/ml/relapse-risk")
      ])

      setUserInfo(userRes.data)
      setPrediction(predRes.data)
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to load dashboard")
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("user_id")
    navigate("/")
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return "#22c55e"     // green
    if (score < 70) return "#f59e0b"     // yellow
    return "#ef4444"                     // red
  }

  return (
    <div className="page-center">
      <div style={{ width: "100%", maxWidth: 520 }}>

        {/* HEADER */}
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
          <h2>🌊 VirtualMukti</h2>
          <button className="secondary-btn" style={{width:"200px"}} onClick={handleLogout}>
            Logout
          </button>
        </div>

        {error && (
          <div className="glass-card" style={{ marginBottom: 16 }}>
            <p style={{ color: "var(--danger)" }}>{error}</p>
          </div>
        )}

        {/* USER INFO CARD */}
        <div className="glass-card fade-in">
          <h3>👋 Welcome back</h3>

          {userInfo ? (
            <>
              <p><b>Username:</b> {userInfo.username}</p>
              <p><b>Language:</b> {userInfo.language_preference}</p>
              <p><b>Sobriety Streak:</b> {userInfo.recovery_streak} days</p>
            </>
          ) : (
            <p>Loading your profile...</p>
          )}
        </div>

        {/* RELAPSE RISK CARD */}
        <div className="glass-card fade-in" style={{ marginTop: 16 }}>
          <h3>📊 Relapse Risk</h3>

          {prediction ? (
            <>
              <div style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: 8
              }}>
                <span>Risk Score</span>
                <b>{prediction.risk_score}%</b>
              </div>

              <div style={{
                height: 10,
                background: "#e5e7eb",
                borderRadius: 20,
                overflow: "hidden"
              }}>
                <div
                  style={{
                    width: `${prediction.risk_score}%`,
                    height: "100%",
                    background: getRiskColor(prediction.risk_score),
                    transition: "0.4s ease"
                  }}
                />
              </div>

              <p style={{ marginTop: 10 }}>
                <b>Level:</b> {prediction.risk_level}
              </p>

              <button
                className="secondary-btn"
                style={{ marginTop: 12 }}
                onClick={loadDashboard}
              >
                Refresh
              </button>
            </>
          ) : (
            <p>Analyzing your recent patterns...</p>
          )}
        </div>

        {/* ACTIONS CARD */}
        <div className="glass-card fade-in" style={{ marginTop: 16 }}>
          <h3>🧭 What would you like to do?</h3>

          <button
            className="primary-btn"
            onClick={() => navigate("/chatbot")}
            style={{ marginTop: 12 }}
          >
            💬 Talk to AI Counselor
          </button>

          <button
            className="secondary-btn"
            onClick={() => navigate("/mood-checkin")}
            style={{ marginTop: 12 }}
          >
            🧘 Daily Mood Check-In
          </button>
        </div>

      </div>
    </div>
  )
}
