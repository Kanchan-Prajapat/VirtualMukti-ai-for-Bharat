import { useEffect, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

export default function Stories() {
  const [stories, setStories] = useState<any[]>([])

  useEffect(() => {
    const fetchStories = async () => {
      const res = await api.get("/api/stories")
      setStories(res.data)
    }
    fetchStories()
  }, [])

  return (
    <>
       <Navbar />
    
    <div className="page-center">
      <div style={{ maxWidth: 800, width: "100%" }}>
     
        <div className="glass-card">
          <h2>🌱 Real Recovery Stories</h2>
        </div>

        {stories.map((story, index) => (
          <div key={index} className="glass-card fade-in" style={{ marginTop: 20 }}>
            <h3>{story.title}</h3>
            <p>{story.story}</p>
          </div>
        ))}
      </div>
    </div>

    </>
  )
}