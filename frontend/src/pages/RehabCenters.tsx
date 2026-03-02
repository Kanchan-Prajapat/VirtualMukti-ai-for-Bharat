import { useEffect, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function RehabCenters() {
  const [centers, setCenters] = useState<any[]>([])
  const [city, setCity] = useState("")

  const loadCenters = async () => {
    try {
      const res = await api.get(`/api/rehab?city=${city}`)
      setCenters(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    loadCenters()
  }, [])

  return (
    <>
      <Navbar />

      <div className="rehab-wrapper">
        <div className="rehab-content">

          {/* Search Section */}
          <div className="glass-card">
            <h2>🏥 Rehab Centers</h2>

            <div className="rehab-search">
              <input
                placeholder="Search by city (e.g. Delhi)"
                value={city}
                onChange={(e) => setCity(e.target.value)}
              />

              <button
                className="primary-btn"
                onClick={loadCenters}
              >
                Search
              </button>
            </div>
          </div>

          {/* Results Grid */}
          <div className="rehab-grid">
            {centers.map((center, index) => (
              <div key={index} className="glass-card rehab-card">
                <h3>{center.name}</h3>

                <p><strong>City:</strong> {center.city}</p>
                <p><strong>Phone:</strong> {center.phone}</p>
                <p><strong>Type:</strong> {center.type}</p>

                {center.website && (
                  <a
                    href={center.website}
                    target="_blank"
                    rel="noreferrer"
                    className="rehab-link"
                  >
                    Visit Website →
                  </a>
                )}
              </div>
            ))}
          </div>

        </div>
      </div>
    </>
  )
}