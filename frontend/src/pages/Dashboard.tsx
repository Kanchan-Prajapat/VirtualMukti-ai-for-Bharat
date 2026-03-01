import { useEffect, useState } from "react"
import api from "../config/api"
import { useNavigate } from "react-router-dom"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function Dashboard() {
  const [userInfo, setUserInfo] = useState<any>(null)
  const [prediction, setPrediction] = useState<any>(null)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      navigate("/")
      return
    }
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
    localStorage.clear()
    navigate("/")
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return "#22c55e"
    if (score < 70) return "#f59e0b"
    return "#ef4444"
  }

  return (
    <div className="page-container">
    <div style={{ minHeight: "100vh", paddingBottom: 60 }}>

       <Navbar />

      <div style={{
        maxWidth: 900,
        margin: "40px auto",
        padding: "0 20px"
      }}>

        {/* Welcome Section */}
        <div className="glass-card fade-in">
          <h2>
            👋 Welcome back {userInfo?.username && `@${userInfo.username}`}
          </h2>
          <p>
            Your recovery journey is one step stronger today.
          </p>
          {userInfo && (
            <div style={{ marginTop: 12 }}>
              <p>Language: {userInfo.language_preference}</p>
              <p>
                Sobriety Streak: 
                <strong> {userInfo.recovery_streak} days</strong>
              </p>
            </div>
          )}
        </div>

        {/* Relapse Risk Card */}
        <div className="glass-card fade-in" style={{ marginTop: 30 }}>
          <h3>📊 Relapse Risk Analysis</h3>

          {prediction ? (
            <>
              <div style={{
                display: "flex",
                justifyContent: "space-between",
                marginTop: 16
              }}>
                <span>Risk Score</span>
                <strong>{prediction.risk_score}%</strong>
              </div>

              <div style={{
                height: 14,
                background: "#e2e8f0",
                borderRadius: 50,
                marginTop: 10,
                overflow: "hidden"
              }}>
                <div
                  style={{
                    width: `${prediction.risk_score}%`,
                    height: "100%",
                    background: getRiskColor(prediction.risk_score),
                    transition: "0.6s ease"
                  }}
                />
              </div>

              <p style={{ marginTop: 16 }}>
                Risk Level: <strong>{prediction.risk_level}</strong>
              </p>

              <button
                className="primary-btn"
                style={{ marginTop: 16 }}
                onClick={loadDashboard}
              >
                Refresh Analysis
              </button>
            </>
          ) : (
            <p>Analyzing your recent patterns...</p>
          )}
        </div>

        {/* ===== Recovery Action Grid ===== */}
        <div style={{
          marginTop: 40,
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: 20
        }}>

          <div className="glass-card">
            <h4>💬 AI Counselor</h4>
            <p>Talk anytime with your CBT-based recovery assistant.</p>
            <button
              className="primary-btn"
              style={{ marginTop: 12 }}
              onClick={() => navigate("/chatbot")}
            >
              Start Chat
            </button>
          </div>

          <div className="glass-card">
            <h4>🏥 Nearby Rehab Centers</h4>
            <p>Find verified rehabilitation centers near you.</p>
            <button
              className="primary-btn"
              style={{ marginTop: 12 }}
              onClick={() => navigate("/rehab")}
            >
              Explore Centers
            </button>
          </div>

          <div className="glass-card">
            <h4>📞 Helplines</h4>
            <p>Access 24/7 addiction support and crisis contacts.</p>
            <button
              className="primary-btn"
              style={{ marginTop: 12 }}
              onClick={() => navigate("/helplines")}
            >
              View Contacts
            </button>
          </div>

          <div className="glass-card">
            <h4>🌱 Recovery Stories</h4>
            <p>Read real stories of people who overcame addiction.</p>
            <button
              className="primary-btn"
              style={{ marginTop: 12 }}
              onClick={() => navigate("/stories")}
            >
              Read Stories
            </button>
          </div>

          <div className="glass-card">
            <h4>✨ Daily Motivation</h4>
            <p>AI-generated positive quotes to stay strong.</p>
            <button
              className="primary-btn"
              style={{ marginTop: 12 }}
              onClick={() => navigate("/motivation")}
            >
              Get Inspired
            </button>
          </div>

        </div>

      </div>
    </div>
    </div>
  )
}