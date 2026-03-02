import { useEffect, useState } from "react"
import api from "../config/api"
import { useNavigate } from "react-router-dom"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function Dashboard() {
  const [userInfo, setUserInfo] = useState<any>(null)
  const [prediction, setPrediction] = useState<any>(null)
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
    } catch (err) {
      console.error("Dashboard load failed:", err)
    }
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return "#22c55e"
    if (score < 70) return "#f59e0b"
    return "#ef4444"
  }

  return (
    <>
      <Navbar />

      <div className="dashboard-wrapper">
        <div className="dashboard-content">

          {/* ================= Welcome Card ================= */}
        {/* ================= Top Row (Welcome + Risk) ================= */}
<div className="dashboard-top-row">

  {/* Welcome Card */}
  <div className="glass-card fade-in">
    <h2>
      👋 Welcome back{" "}
      {userInfo?.username && `@${userInfo.username}`}
    </h2>

    <p>Your recovery journey is one step stronger today.</p>

    {userInfo && (
      <div className="info-block">
        <p>Language: {userInfo.language_preference}</p>
        <p>
          Sobriety Streak:
          <strong> {userInfo.recovery_streak} days</strong>
        </p>
      </div>
    )}
  </div>

  {/* Risk Analysis */}
  <div className="glass-card fade-in">
    <h3>📊 Relapse Risk Analysis</h3>

    {prediction ? (
      <>
        <div className="risk-row">
          <span>Risk Score</span>
          <strong>{prediction.risk_score}%</strong>
        </div>

        <div className="risk-bar">
          <div
            className="risk-fill"
            style={{
              width: `${prediction.risk_score}%`,
              background: getRiskColor(prediction.risk_score)
            }}
          />
        </div>

        <p>
          Risk Level:{" "}
          <strong>{prediction.risk_level}</strong>
        </p>

        <button
          className="primary-btn"
          onClick={loadDashboard}
        >
          Refresh Analysis
        </button>
      </>
    ) : (
      <p>Analyzing your recent patterns...</p>
    )}
  </div>

</div>

          {/* ================= Action Grid ================= */}
          <div className="dashboard-grid">

            <div className="glass-card">
              <h4>💬 AI Counselor</h4>
              <p>Talk anytime with your CBT-based recovery assistant.</p>
              <button
                className="primary-btn"
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
                onClick={() => navigate("/motivation")}
              >
                Get Inspired
              </button>
            </div>

          </div>

        </div>
      </div>
    </>
  )
}