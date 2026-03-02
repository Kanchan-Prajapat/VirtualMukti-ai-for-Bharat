import { useEffect, useRef, useState } from "react"
import api from "../config/api"
import "../../styles/theme.css"
import Navbar from "../components/Navbar"
import {
  getMessages,
  addMessage as storeAddMessage,
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

  // const handleClear = () => {
  //   clearMessages(userId)
  //   setMessages([])
  // }

 return (
  <>
    <Navbar />

    <div className="chat-wrapper">

      {/* Chat Messages Area */}
      <div className="chat-container">

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-row ${
              msg.sender === "user" ? "chat-user" : "chat-bot"
            }`}
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
                <div className="crisis-warning">
                  ⚠ Crisis detected — please seek immediate help.
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-row chat-bot">
            <div className="chat-bubble-bot typing">
              Typing...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
     <form onSubmit={handleSend} className="chat-input-area">
  <div className="chat-input-container">
    <textarea
      value={message}
      onChange={e => setMessage(e.target.value)}
      placeholder="Share what's on your mind..."
    />

    <button
      type="submit"
      className="primary-btn"
      disabled={loading}
    >
      {loading ? "Sending..." : "Send"}
    </button>
  </div>
</form>

    </div>
  </>
)
}