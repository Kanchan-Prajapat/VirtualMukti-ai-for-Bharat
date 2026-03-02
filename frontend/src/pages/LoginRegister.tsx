import api from "../config/api"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"

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
    const res = await api.post("/api/auth/login", {
      username: username.toLowerCase(),
      password
    })

    // ✅ SAVE TOKEN
    localStorage.setItem("token", res.data.token)
    localStorage.setItem("user_id", res.data.user_id)
    window.location.href = "/dashboard"

    navigate("/dashboard")

  } catch (err: any) {
    const msg = err?.response?.data?.detail || "Invalid username or password"
    setError(msg)
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
    const res = await api.post("/api/auth/register", {
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

    // ✅ SAVE TOKEN AFTER REGISTER
    localStorage.setItem("token", res.data.token)
    localStorage.setItem("user_id", res.data.user_id)
    window.location.href = "/dashboard"

    navigate("/dashboard")

  } catch (err: any) {
    const msg = err?.response?.data?.detail || "Registration failed"
    setError(msg)
  }
}



  return (
    <div className="page-center">
      <div className="glass-card fade-in" style={{ maxWidth: 420, width: "100%" }}>
        <Navbar />
        
        <div style={{ textAlign: "center", marginBottom: 20 }}>
          <h1 style={{ fontSize: 28, fontWeight: 700 }}>
  VirtualMukti
</h1>
<p style={{ fontSize: 14, color: "var(--muted)", marginTop: 6 }}>
  Your AI-powered recovery companion
</p>
          <p style={{ fontSize: 14 }}>
            {isLogin
              ? "Welcome back to your recovery journey."
              : "A safe, intelligent space for healing."}
          </p>
        </div>

        <form onSubmit={isLogin ? handleLogin : handleRegister}>
          <input
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />

          {!isLogin && (
            <>
              <input
                type="number"
                placeholder="Age"
                value={age}
                onChange={e => setAge(e.target.value)}
                required
              />

              <input
                placeholder="Gender"
                value={gender}
                onChange={e => setGender(e.target.value)}
                required
              />

              <input
                placeholder="City"
                value={location}
                onChange={e => setLocation(e.target.value)}
                required
              />
            </>
          )}

          <button className="primary-btn" style={{ marginTop: 20 }}>
            {isLogin ? "Login" : "Create Account"}
          </button>
        </form>

        <button
          className="primary-btn"
          style={{ marginTop: 16 }}
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "New here? Register" : "Already have an account?"}
        </button>

        {error && (
          <p style={{ color: "var(--danger)", marginTop: 14 }}>
            {error}
          </p>
        )}
      </div>
    </div>
  )
}