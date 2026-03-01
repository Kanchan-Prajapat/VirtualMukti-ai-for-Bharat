import { useEffect, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function RehabCenters() {
  const [centers, setCenters] = useState<any[]>([])
  const [city, setCity] = useState("")

  const loadCenters = async () => {
    const res = await api.get(`/api/rehab?city=${city}`)
    setCenters(res.data)
  }

  useEffect(() => {
    loadCenters()
  }, [])

  return (
    <div className="page-center">
      <div style={{ maxWidth: 800, width: "100%" }}>
        <Navbar />
        <div className="glass-card">
          <h2>🏥 Verified Rehab Centers</h2>

          <input
            placeholder="Search by city (e.g. Delhi)"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <button
            className="primary-btn"
            style={{ marginTop: 12 }}
            onClick={loadCenters}
          >
            Search
          </button>
        </div>

        {centers.map((center, index) => (
          <div key={index} className="glass-card fade-in" style={{ marginTop: 20 }}>
            <h3>{center.name}</h3>
            <p><strong>City:</strong> {center.city}</p>
            <p><strong>Phone:</strong> {center.phone}</p>
            <p><strong>Type:</strong> {center.type}</p>
            <a href={center.website} target="_blank" rel="noreferrer">
              Visit Website
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}