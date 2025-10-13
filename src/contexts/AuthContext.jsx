import { createContext, useContext, useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import api from '../services/api'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkSession()
  }, [])

  const checkSession = async () => {
    try {
      const userData = JSON.parse(localStorage.getItem('user'))
      if (userData) {
        setUser(userData)
      }
    } catch (error) {
      console.error('Session check failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })
      const userData = response.data
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
      toast.success('Welcome back!')
      return userData
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
      throw new Error(message)
    }
  }

  const signup = async (name, email, password, plan = 'free') => {
    try {
      const response = await api.post('/auth/signup', { 
        name, 
        email, 
        password, 
        plan 
      })
      const userData = response.data
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
      toast.success('Account created successfully!')
      return userData
    } catch (error) {
      const message = error.response?.data?.detail || 'Signup failed'
      toast.error(message)
      throw new Error(message)
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
    toast.success('Logged out successfully')
  }

  const canCreateOffer = () => {
    if (!user) return false
    const limits = { free: 1, professional: 4, enterprise: Infinity }
    return (user.offerCount || 0) < limits[user.plan]
  }

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    isAuthenticated: !!user,
    canCreateOffer
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
