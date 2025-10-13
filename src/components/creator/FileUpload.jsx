import { useState, useCallback } from 'react'
import { Upload, File, X, CheckCircle } from 'lucide-react'

export default function FileUpload({ onProcessed }) {
  const [file, setFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const [processing, setProcessing] = useState(false)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }, [])

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file) => {
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ]
    
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF, DOCX, or TXT file')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB')
      return
    }

    setFile(file)
  }

  const processFile = async () => {
    setProcessing(true)

    // Simulate file processing
    setTimeout(() => {
      // In production, this would call the backend API
      const extractedData = {
        title: 'Redesigned Professional Service Offer',
        subtitle: 'Enhanced and optimized for maximum conversion',
        description: 'Your offer has been analyzed and enhanced with AI-powered improvements to increase engagement and close rates.',
        price: { amount: 997, currency: 'USD', interval: 'one-time' },
        features: [
          'Enhanced feature presentation',
          'Improved value proposition',
          'Optimized pricing display',
          'Professional design elements'
        ]
      }

      onProcessed(extractedData)
    }, 2000)
  }

  const removeFile = () => {
    setFile(null)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Upload Your Existing Offer
        </h2>
        <p className="text-gray-600 text-lg">
          We'll analyze it and create a stunning redesign
        </p>
      </div>

      {!file ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-3 border-dashed rounded-2xl p-12 text-center transition-all ${
            dragActive
              ? 'border-primary-600 bg-primary-50'
              : 'border-gray-300 bg-white'
          }`}
        >
          <div className="flex flex-col items-center">
            <div className="bg-primary-100 p-6 rounded-full mb-6">
              <Upload className="w-12 h-12 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Drop your file here, or browse
            </h3>
            <p className="text-gray-500 mb-6">
              Supports PDF, DOCX, TXT (max 10MB)
            </p>
            <label className="cursor-pointer">
              <span className="bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors inline-block">
                Browse Files
              </span>
              <input
                type="file"
                onChange={handleChange}
                accept=".pdf,.docx,.txt"
                className="hidden"
              />
            </label>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="bg-primary-100 p-3 rounded-lg">
                <File className="w-8 h-8 text-primary-600" />
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">{file.name}</h4>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            {!processing && (
              <button
                onClick={removeFile}
                className="text-gray-400 hover:text-red-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            )}
          </div>

          {processing ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Analyzing your offer...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a moment</p>
            </div>
          ) : (
            <button
              onClick={processFile}
              className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
            >
              <CheckCircle className="w-5 h-5" />
              Process & Redesign
            </button>
          )}
        </div>
      )}
    </div>
  )
}
