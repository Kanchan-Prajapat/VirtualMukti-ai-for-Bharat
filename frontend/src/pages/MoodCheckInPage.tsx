import { useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"

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
        <div className="glass-card fade-in">
          <h2>🌱 Check-in Complete</h2>
          <p>You showed up today. That matters.</p>
          <a href="/dashboard" className="primary-btn" style={{ textDecoration: "none", display: "block", textAlign: "center", marginTop: 16 }}>
            Back to Dashboard
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="page-center">
      <div className="glass-card fade-in" style={{ maxWidth: 480, width: "100%" }}>
        <h2>Daily Check-In</h2>

        {/* Mood */}
        <div style={{ marginTop: 20 }}>
          <p>How are you feeling today?</p>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            {["😔","😕","😐","🙂","😊"].map((emoji, index) => (
              <button
                key={index}
                onClick={() => setMood(index + 1)}
                className="secondary-btn"
                style={{
                  fontSize: 24,
                  background: mood === index + 1 ? "#111827" : "#f3f4f6",
                  color: mood === index + 1 ? "#fff" : "#111827"
                }}
              >
                {emoji}
              </button>
            ))}
          </div>
        </div>

        {/* Craving */}
        <div style={{ marginTop: 24 }}>
          <p>Craving intensity: <b>{craving}/10</b></p>
          <input
            type="range"
            min={0}
            max={10}
            value={craving}
            onChange={e => setCraving(Number(e.target.value))}
          />
        </div>

        {/* Triggers */}
        <div style={{ marginTop: 24 }}>
          <p>Any triggers today?</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {allTriggers.map(t => (
              <button
                key={t}
                onClick={() => toggleTrigger(t)}
                className="secondary-btn"
                style={{
                  background: triggers.includes(t) ? "#111827" : "#ffffff",
                  color: triggers.includes(t) ? "#ffffff" : "#111827"
                }}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        <button
          disabled={!mood}
          onClick={submitCheckIn}
          className="primary-btn"
          style={{ marginTop: 28, opacity: mood ? 1 : 0.5 }}
        >
          Submit Check-In
        </button>
      </div>
    </div>
  )
}
