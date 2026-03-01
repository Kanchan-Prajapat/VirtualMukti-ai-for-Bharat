import { useState, useEffect } from 'react'
import LoginRegister from './pages/LoginRegister'
import Dashboard from './pages/Dashboard'
import Chatbot from './pages/Chatbot'
import { Route, Routes } from 'react-router-dom'
import MoodCheckInPage from "./pages/MoodCheckInPage"
import RehabCenters from "./pages/RehabCenters"
import Helplines from "./pages/Helplines"
import Stories from "./pages/Stories"
import Motivation from "./pages/Motivation"


function App() {
  const [page, setPage] = useState('login')

  useEffect(() => {
    // Simple routing based on URL path
    const path = window.location.pathname
    if (path === '/dashboard') setPage('dashboard')
    else if (path === '/chatbot') setPage('chatbot')
    else setPage('login')
  }, [])

  // Update URL when page changes
  const navigate = (newPage: string) => {
    setPage(newPage)
    window.history.pushState({}, '', `/${newPage === 'login' ? '' : newPage}`)
  }

  return (
    <div>
     <Routes>
     <Route path="/" element={<LoginRegister />} />
     <Route path="/dashboard" element={<Dashboard />} />
     <Route path="/chatbot" element={<Chatbot />} />
     <Route path="/mood-checkin" element={<MoodCheckInPage />} />
     <Route path="/rehab" element={<RehabCenters />} />
<Route path="/helplines" element={<Helplines />} />
<Route path="/stories" element={<Stories />} />
<Route path="/motivation" element={<Motivation />} />
    </Routes>
    </div>
  )
}

export default App
