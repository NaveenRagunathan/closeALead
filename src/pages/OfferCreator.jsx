import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import ModeSelector from '../components/creator/ModeSelector'
import AIChat from '../components/creator/AIChat'
import FileUpload from '../components/creator/FileUpload'
import TemplateSelector from '../components/creator/TemplateSelector'
import CustomizationPanel from '../components/creator/CustomizationPanel'
import LivePreview from '../components/creator/LivePreview'
import api from '../services/api'
import toast from 'react-hot-toast'

export default function OfferCreator() {
  const { offerId } = useParams()
  const navigate = useNavigate()
  const [mode, setMode] = useState(null) // 'scratch' or 'redesign'
  const [step, setStep] = useState('mode') // 'mode', 'input', 'template', 'customize'
  const [offerData, setOfferData] = useState({
    title: '',
    subtitle: '',
    description: '',
    clientName: '',
    price: { amount: 0, currency: 'USD', interval: 'one-time' },
    features: [],
    template: 'modern',
    brandColors: { primary: '#3b82f6', secondary: '#8b5cf6', accent: '#10b981' },
    logoUrl: '',
    images: [],
    editCount: 0,
    editLimit: 5
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (offerId) {
      loadExistingOffer()
    }
  }, [offerId])

  const loadExistingOffer = async () => {
    try {
      const response = await api.get(`/offers/${offerId}`)
      setOfferData(response.data)
      setStep('customize')
    } catch (error) {
      toast.error('Failed to load offer')
      navigate('/dashboard')
    }
  }

  const handleModeSelect = (selectedMode) => {
    setMode(selectedMode)
    setStep('input')
  }

  const handleAIComplete = (aiGeneratedData) => {
    setOfferData({ ...offerData, ...aiGeneratedData })
    setStep('template')
  }

  const handleFileProcessed = (extractedData) => {
    setOfferData({ ...offerData, ...extractedData })
    setStep('template')
  }

  const handleTemplateSelect = (template) => {
    setOfferData({ ...offerData, template })
    setStep('customize')
  }

  const handleDataChange = (field, value) => {
    setOfferData({ ...offerData, [field]: value })
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      if (offerId) {
        await api.put(`/offers/${offerId}`, offerData)
        toast.success('Offer updated successfully!')
      } else {
        const response = await api.post('/offers', offerData)
        toast.success('Offer created successfully!')
        navigate(`/edit/${response.data.id}`)
      }
    } catch (error) {
      toast.error('Failed to save offer')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const response = await api.post(`/offers/${offerId}/export`, {}, {
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${offerData.title || 'offer'}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('PDF exported successfully!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-30">
        <div className="max-w-full px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="w-6 h-6" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  {offerId ? 'Edit Offer' : 'Create New Offer'}
                </h1>
                {step === 'customize' && (
                  <p className="text-sm text-gray-600">
                    Edits: {offerData.editCount}/{offerData.editLimit}
                  </p>
                )}
              </div>
            </div>
            {step === 'customize' && (
              <div className="flex gap-3">
                <button
                  onClick={handleSave}
                  disabled={loading}
                  className="px-6 py-2 bg-gray-100 text-gray-900 rounded-lg font-medium hover:bg-gray-200 transition-colors"
                >
                  Save Draft
                </button>
                {offerId && (
                  <button
                    onClick={handleExport}
                    className="px-6 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
                  >
                    Export as PDF
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-full">
        {step === 'mode' && (
          <div className="max-w-4xl mx-auto px-6 py-12">
            <ModeSelector onSelect={handleModeSelect} />
          </div>
        )}

        {step === 'input' && (
          <div className="max-w-4xl mx-auto px-6 py-12">
            {mode === 'scratch' ? (
              <AIChat onComplete={handleAIComplete} />
            ) : (
              <FileUpload onProcessed={handleFileProcessed} />
            )}
          </div>
        )}

        {step === 'template' && (
          <div className="max-w-6xl mx-auto px-6 py-12">
            <TemplateSelector
              selectedTemplate={offerData.template}
              onSelect={handleTemplateSelect}
            />
          </div>
        )}

        {step === 'customize' && (
          <div className="flex">
            <CustomizationPanel
              data={offerData}
              onChange={handleDataChange}
            />
            <LivePreview data={offerData} />
          </div>
        )}
      </main>
    </div>
  )
}
