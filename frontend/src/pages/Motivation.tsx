import { useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function Motivation() {
  const [quote, setQuote] = useState("")

  const getQuote = async () => {
    const res = await api.get("/api/motivation/quote")
    setQuote(res.data.quote)
  }

  return (
    <> <Navbar />
  
    <div className="page-center">
      <div style={{ maxWidth: 600, width: "100%" }}>
       
        <div className="glass-card" style={{ textAlign: "center" }}>
          <h2>✨ Daily Motivation</h2>

          <button
            className="primary-btn"
            style={{ marginTop: 20 }}
            onClick={getQuote}
          >
            Generate Quote
          </button>

          {quote && (
            <p style={{
              marginTop: 24,
              fontSize: 18,
              fontWeight: 500
            }}>
              “{quote}”
            </p>
          )}
        </div>
      </div>
    </div>
      </>
  )
}