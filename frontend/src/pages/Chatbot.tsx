import { useEffect, useRef, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"

export default function Chatbot() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<any[]>([])
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    const userMsg = { sender: "user", text: message }
    setMessages(prev => [...prev, userMsg])
    setMessage("")

    const res = await api.post("/api/chatbot/message", { message })
    const botMsg = { sender: "bot", text: res.data.response }
    setMessages(prev => [...prev, botMsg])
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <div style={{ padding: 20, borderBottom: "1px solid #e5e7eb" }}>
        <h2>AI Counselor</h2>
      </div>

      <div style={{ flex: 1, padding: 20 }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              marginBottom: 12
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
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSend} style={{ padding: 20, borderTop: "1px solid #e5e7eb" }}>
        <textarea
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Share what's on your mind..."
        />
        <button className="primary-btn" style={{ marginTop: 10 }}>
          Send
        </button>
      </form>
    </div>
  )
}
