import api from "../config/api"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "../../styles/theme.css"

export default function LoginRegister() {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [age, setAge] = useState("")
  const [gender, setGender] = useState("")
  const [location, setLocation] = useState("")
  const [error, setError] = useState("")
  const navigate = useNavigate()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    try {
      await api.post("/api/auth/login", {
        username: username.toLowerCase(),
        password
      })
      navigate("/dashboard")
    } catch {
      setError("Invalid username or password")
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    const parsedAge = Number(age)
    if (!parsedAge || parsedAge <= 0) {
      setError("Please enter a valid age")
      return
    }

    try {
      await api.post("/api/auth/register", {
        username,
        password,
        demographics: {
          age: parsedAge,
          gender,
          location,
          addiction_type: "alcohol",
          severity: "moderate"
        },
        language_preference: "english",
        consent_given: true
      })
      navigate("/dashboard")
    } catch {
      setError("Registration failed")
    }
  }

  return (
    <div className="page-center">
      <div className="glass-card fade-in" style={{ maxWidth: 400, width: "100%" }}>
        <h1>🌊 VirtualMukti</h1>
        <p>{isLogin ? "Welcome back." : "A safe space for recovery."}</p>

        <form onSubmit={isLogin ? handleLogin : handleRegister}>
          <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />

          {!isLogin && (
            <>
              <input type="number" placeholder="Age" value={age} onChange={e => setAge(e.target.value)} required />
              <input placeholder="Gender" value={gender} onChange={e => setGender(e.target.value)} required />
              <input placeholder="City" value={location} onChange={e => setLocation(e.target.value)} required />
            </>
          )}

          <button className="primary-btn" style={{ marginTop: 16 }}>
            {isLogin ? "Login" : "Create Account"}
          </button>
        </form>

        <button className="secondary-btn" style={{ marginTop: 16 }} onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "New here? Register" : "Already have an account?"}
        </button>

        {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      </div>
    </div>
  )
}
