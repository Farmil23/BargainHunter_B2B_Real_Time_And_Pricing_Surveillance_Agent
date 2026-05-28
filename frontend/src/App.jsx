import './App.css'
import LandingPage from './components/LandingPage'
import Dashboard from './components/Dashboard'

function App() {
  const path = window.location.pathname

  if (path === '/dashboard') {
    return <Dashboard />
  }

  return <LandingPage />
}

export default App
