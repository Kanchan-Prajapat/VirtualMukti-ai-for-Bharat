import { useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function MoodCheckInPage() {
  const [mood, setMood] = useState<number | null>(null)
  const [craving, setCraving] = useState(3)
  const [triggers, setTriggers] = useState<string[]>([])
  const [success, setSuccess] = useState(false)

  const allTriggers = [
    "Stress",
    "Loneliness",
    "Boredom",
    "Social pressure",
    "Anxiety",
    "Anger"
  ]

  const toggleTrigger = (trigger: string) => {
    setTriggers(prev =>
      prev.includes(trigger)
        ? prev.filter(t => t !== trigger)
        : [...prev, trigger]
    )
  }

  const submitCheckIn = async () => {
    await api.post("/api/activity/checkin", {
      mood_score: mood,
      craving_intensity: craving,
      triggers_encountered: triggers
    })
    setSuccess(true)
  }

  if (success) {
    return (
      <div className="page-center">
        <div className="glass-card fade-in" style={{ maxWidth: 480, textAlign: "center" }}>
          <h2>🌱 Check-in Complete</h2>
          <p style={{ marginTop: 8 }}>
            You showed up for yourself today. That’s strength.
          </p>

          <a
            href="/dashboard"
            className="primary-btn"
            style={{
              textDecoration: "none",
              display: "block",
              textAlign: "center",
              marginTop: 24
            }}
          >
            Back to Dashboard
          </a>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: "100vh" }}>
      
      {/* Header */}
       <Navbar />
        <div className="glass-card fade-in">

          {/* SECTION 1: MOOD */}
          <div>
            <h3>How are you feeling today?</h3>

            <div style={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: 20
            }}>
              {["😔","😕","😐","🙂","😊"].map((emoji, index) => (
                <button
                  key={index}
                  onClick={() => setMood(index + 1)}
                  style={{
                    fontSize: 28,
                    borderRadius: 20,
                    border: mood === index + 1
                      ? "2px solid var(--primary)"
                      : "1px solid var(--border)",
                    background: "#ffffff",
                    width: 60,
                    height: 60,
                    transition: "all 0.2s ease",
                    transform: mood === index + 1 ? "scale(1.1)" : "scale(1)"
                  }}
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>

          {/* SECTION 2: CRAVING */}
          <div style={{ marginTop: 40 }}>
            <h3>Craving intensity</h3>
            <p style={{ fontSize: 14 }}>
              Current level: <strong>{craving}/10</strong>
            </p>

            <input
              type="range"
              min={0}
              max={10}
              value={craving}
              onChange={e => setCraving(Number(e.target.value))}
              style={{ marginTop: 12 }}
            />
          </div>

          {/* SECTION 3: TRIGGERS */}
          <div style={{ marginTop: 40 }}>
            <h3>Any triggers today?</h3>

            <div style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 12,
              marginTop: 16
            }}>
              {allTriggers.map(t => (
                <button
                  key={t}
                  onClick={() => toggleTrigger(t)}
                  style={{
                    padding: "10px 18px",
                    borderRadius: 999,
                    border: triggers.includes(t)
                      ? "1px solid var(--primary)"
                      : "1px solid var(--border)",
                    background: triggers.includes(t)
                      ? "var(--primary)"
                      : "#ffffff",
                    color: triggers.includes(t)
                      ? "#ffffff"
                      : "var(--text)",
                    fontSize: 14,
                    transition: "all 0.2s ease"
                  }}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* SUBMIT */}
          <button
            disabled={!mood}
            onClick={submitCheckIn}
            className="primary-btn"
            style={{
              marginTop: 48,
              opacity: mood ? 1 : 0.5
            }}
          >
            Submit Check-In
          </button>

        </div>
      </div>
  )
}