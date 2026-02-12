type ChatMessage = {
  sender: 'user' | 'bot'
  text: string
  timestamp: number
  crisis_detected?: boolean
}

const KEY = 'chat_history'

export const getMessages = (): ChatMessage[] => {
  const raw = localStorage.getItem(KEY)
  return raw ? JSON.parse(raw) : []
}

export const addMessage = (msg: ChatMessage) => {
  const messages = getMessages()
  messages.push(msg)
  localStorage.setItem(KEY, JSON.stringify(messages))
}
