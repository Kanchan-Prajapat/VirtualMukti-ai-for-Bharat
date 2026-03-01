import { useEffect, useRef, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import {
  getMessages,
  addMessage as storeAddMessage,
  clearMessages
} from "../store/chatStore"
export default function Chatbot() {

  

  const userId = localStorage.getItem("user_id") || "anonymous"

  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState(getMessages(userId))
  const [loading, setLoading] = useState(false)

  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(()=>{
    if(!localStorage.getItem("token"))
    {
      window.location.href ="/"
    }
  })

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    const userMsg = {
      sender: "user" as const,
      text: message,
      timestamp: Date.now()
    }

    // Save to store
    storeAddMessage(userId, userMsg)
    setMessages(getMessages(userId))
    setMessage("")
    setLoading(true)

    try {
      const res = await api.post("/api/chatbot/message", {
        message: userMsg.text
      })

      const botMsg = {
        sender: "bot" as const,
        text: res.data.response,
        timestamp: Date.now(),
        crisis_detected: res.data.crisis_detected
      }

      storeAddMessage(userId, botMsg)
      setMessages(getMessages(userId))

    } catch {
      const errorMsg = {
        sender: "bot" as const,
        text: "Something went wrong. Please try again.",
        timestamp: Date.now()
      }

      storeAddMessage(userId, errorMsg)
      setMessages(getMessages(userId))
    }

    setLoading(false)
  }

  const handleClear = () => {
    clearMessages(userId)
    setMessages([])
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>

      {/* Header */}
      <div className="app-header">
        <div className="app-title">🌊 VirtualMukti AI Counselor</div>
        <button
          className="secondary-btn"
          style={{ width: 140 }}
          onClick={handleClear}
        >
          Clear Chat
        </button>
      </div>

      {/* Chat Area */}
      <div style={{
        flex: 1,
        display: "flex",
        justifyContent: "center",
        padding: "40px 20px"
      }}>
        <div style={{ width: "100%", maxWidth: 720 }}>

          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                display: "flex",
                justifyContent:
                  msg.sender === "user" ? "flex-end" : "flex-start",
                marginBottom: 16
              }}
            >
              <div
                className={
                  msg.sender === "user"
                    ? "chat-bubble-user fade-in"
                    : "chat-bubble-bot fade-in"
                }
              >
                {msg.text}

                {msg.crisis_detected && (
                  <div style={{
                    marginTop: 10,
                    fontSize: 12,
                    color: "var(--danger)"
                  }}>
                    ⚠ Crisis detected — please seek immediate help.
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div style={{ marginBottom: 16 }}>
              <div className="chat-bubble-bot">
                Typing...
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input Bar */}
      <form
        onSubmit={handleSend}
        style={{
          padding: 24,
          borderTop: "1px solid #e2e8f0",
          background: "rgba(255,255,255,0.9)",
          backdropFilter: "blur(12px)"
        }}
      >
        <div style={{ maxWidth: 720, margin: "auto" }}>
          <textarea
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="Share what's on your mind..."
          />
          <button
            className="primary-btn"
            style={{ marginTop: 12 }}
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Message"}
          </button>
        </div>
      </form>

    </div>
  )
}