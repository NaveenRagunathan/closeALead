import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Plus, LogOut } from 'lucide-react'
import StatCards from '../components/dashboard/StatCards'
import OfferGrid from '../components/dashboard/OfferGrid'
import api from '../services/api'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { user, logout, canCreateOffer } = useAuth()
  const navigate = useNavigate()
  const [offers, setOffers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOffers()
  }, [])

  const fetchOffers = async () => {
    try {
      const response = await api.get('/offers')
      setOffers(response.data)
    } catch (error) {
      console.error('Failed to fetch offers:', error)
      // For MVP, use mock data if API fails
      setOffers([])
    } finally {
      setLoading(false)
    }
  }

  const handleCreateOffer = () => {
    if (!canCreateOffer()) {
      toast.error('You have reached your offer limit. Please upgrade your plan.')
      return
    }
    navigate('/create')
  }

  const handleEditOffer = (offerId) => {
    navigate(`/edit/${offerId}`)
  }

  const handleDeleteOffer = async (offerId) => {
    if (!window.confirm('Are you sure you want to delete this offer?')) {
      return
    }

    try {
      await api.delete(`/offers/${offerId}`)
      setOffers(offers.filter(offer => offer.id !== offerId))
      toast.success('Offer deleted successfully')
    } catch (error) {
      toast.error('Failed to delete offer')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Welcome back, {user?.name}!</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={handleCreateOffer}
                className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center gap-2"
              >
                <Plus className="w-5 h-5" />
                Create New Offer
              </button>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StatCards user={user} offers={offers} />
        <OfferGrid
          offers={offers}
          onEdit={handleEditOffer}
          onDelete={handleDeleteOffer}
          onCreate={handleCreateOffer}
        />
      </main>
    </div>
  )
}
