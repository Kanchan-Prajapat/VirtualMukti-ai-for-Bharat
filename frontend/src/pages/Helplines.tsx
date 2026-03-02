import { useEffect, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function Helplines() {
  const [helplines, setHelplines] = useState<any[]>([])

  useEffect(() => {
    const fetchData = async () => {
      const res = await api.get("/api/helplines")
      setHelplines(res.data)
    }
    fetchData()
  }, [])

  return (
    <>
        <Navbar />
      
    
    <div className="page-center">
      <div style={{ maxWidth: 700, width: "100%" }}>
    
        <div className="glass-card">
          <h2>📞 National Helplines</h2>
        </div>

        {helplines.map((item, index) => (
          <div key={index} className="glass-card fade-in" style={{ marginTop: 16 }}>
            <h3>{item.name}</h3>
            <p><strong>Number:</strong> {item.number}</p>
            <p><strong>Availability:</strong> {item.available}</p>
          </div>
        ))}
      </div>
    </div>

      </>
  )
}