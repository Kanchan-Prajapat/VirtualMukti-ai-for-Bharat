// chatStore.ts

export type ChatMessage = {
  sender: "user" | "bot"
  text: string
  timestamp: number
  crisis_detected?: boolean
}

const MAX_MESSAGES = 100

const getKey = (userId: string) => `chat_history_${userId}`

// Safe JSON parsing
const safeParse = (value: string | null): ChatMessage[] => {
  try {
    if (!value) return []
    const parsed = JSON.parse(value)
    if (!Array.isArray(parsed)) return []
    return parsed
  } catch {
    return []
  }
}

// Get messages for user
export const getMessages = (userId: string): ChatMessage[] => {
  return safeParse(localStorage.getItem(getKey(userId)))
}

// Save full message list
export const setMessages = (
  userId: string,
  messages: ChatMessage[]
) => {
  const trimmed = messages.slice(-MAX_MESSAGES)
  localStorage.setItem(
    getKey(userId),
    JSON.stringify(trimmed)
  )
}

// Add one message
export const addMessage = (
  userId: string,
  msg: ChatMessage
) => {
  const messages = getMessages(userId)
  messages.push(msg)
  setMessages(userId, messages)
}

// Clear chat for user
export const clearMessages = (userId: string) => {
  localStorage.removeItem(getKey(userId))
}