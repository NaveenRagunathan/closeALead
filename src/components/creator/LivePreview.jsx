import { Check, Maximize2, Minimize2 } from 'lucide-react'
import { useState } from 'react'

export default function LivePreview({ data }) {
  const [zoom, setZoom] = useState('fit')

  const getCurrencySymbol = (currency) => {
    const symbols = { USD: '$', EUR: '€', GBP: '£', CAD: '$' }
    return symbols[currency] || '$'
  }

  const renderModernTemplate = () => (
    <div className="bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 text-white px-12 py-16">
        {data.logoUrl && (
          <img src={data.logoUrl} alt="Logo" className="h-12 mb-8" />
        )}
        <h1 className="text-5xl font-bold mb-4">{data.title || 'Your Offer Title'}</h1>
        <p className="text-xl text-primary-100">{data.subtitle || 'Your subtitle here'}</p>
      </div>

      {/* Description */}
      <div className="px-12 py-12 max-w-4xl">
        <p className="text-gray-700 text-lg leading-relaxed whitespace-pre-wrap">
          {data.description || 'Your detailed description will appear here...'}
        </p>
      </div>

      {/* Features */}
      {data.features.length > 0 && (
        <div className="px-12 py-12 bg-gray-50">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">What You Get</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.features.map((feature, index) => (
              <div key={index} className="flex items-start gap-3 bg-white p-4 rounded-lg">
                <div className="bg-green-100 p-1 rounded-full flex-shrink-0">
                  <Check className="w-5 h-5 text-green-600" />
                </div>
                <span className="text-gray-700">{feature || `Feature ${index + 1}`}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pricing */}
      <div className="px-12 py-16 text-center">
        <div className="inline-block bg-gradient-to-br from-primary-600 to-purple-600 text-white rounded-2xl px-12 py-8">
          <div className="text-sm uppercase tracking-wide mb-2 opacity-90">Investment</div>
          <div className="flex items-baseline justify-center">
            <span className="text-2xl">{getCurrencySymbol(data.price.currency)}</span>
            <span className="text-6xl font-bold">{data.price.amount || 0}</span>
          </div>
          <div className="text-sm mt-2 opacity-90">
            {data.price.interval === 'one-time' ? 'One-time payment' : `per ${data.price.interval}`}
          </div>
          <button className="mt-6 bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
            Get Started Now
          </button>
        </div>
      </div>
    </div>
  )

  const renderBoldTemplate = () => (
    <div className="bg-black text-white">
      {/* Header */}
      <div className="px-12 py-20 text-center border-b-4 border-red-600">
        {data.logoUrl && (
          <img src={data.logoUrl} alt="Logo" className="h-12 mx-auto mb-8 filter invert" />
        )}
        <h1 className="text-6xl font-black mb-6 uppercase tracking-tight">
          {data.title || 'Your Offer Title'}
        </h1>
        <p className="text-2xl text-gray-300">{data.subtitle || 'Your subtitle here'}</p>
      </div>

      {/* Description */}
      <div className="px-12 py-16 max-w-4xl mx-auto">
        <p className="text-gray-300 text-xl leading-relaxed whitespace-pre-wrap">
          {data.description || 'Your detailed description will appear here...'}
        </p>
      </div>

      {/* Features */}
      {data.features.length > 0 && (
        <div className="px-12 py-16 bg-red-600">
          <h2 className="text-4xl font-black text-white mb-8 uppercase text-center">
            What's Included
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {data.features.map((feature, index) => (
              <div key={index} className="flex items-start gap-4 bg-black p-6 rounded-lg">
                <div className="text-red-600 text-2xl font-bold flex-shrink-0">✓</div>
                <span className="text-white text-lg">{feature || `Feature ${index + 1}`}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pricing */}
      <div className="px-12 py-20 text-center">
        <div className="inline-block border-4 border-red-600 rounded-2xl px-16 py-10">
          <div className="text-7xl font-black mb-4">
            {getCurrencySymbol(data.price.currency)}{data.price.amount || 0}
          </div>
          <div className="text-gray-400 text-lg uppercase mb-6">
            {data.price.interval === 'one-time' ? 'One-time' : `Per ${data.price.interval}`}
          </div>
          <button className="bg-red-600 text-white px-10 py-4 rounded-lg font-black text-xl uppercase hover:bg-red-700 transition-colors">
            Claim Now
          </button>
        </div>
      </div>
    </div>
  )

  const renderElegantTemplate = () => (
    <div className="bg-gradient-to-br from-blue-50 to-amber-50">
      {/* Header */}
      <div className="px-12 py-20 text-center">
        {data.logoUrl && (
          <img src={data.logoUrl} alt="Logo" className="h-16 mx-auto mb-8" />
        )}
        <h1 className="text-5xl font-serif font-bold text-blue-900 mb-6">
          {data.title || 'Your Offer Title'}
        </h1>
        <div className="w-24 h-1 bg-amber-600 mx-auto mb-6"></div>
        <p className="text-xl text-blue-800 max-w-2xl mx-auto">
          {data.subtitle || 'Your subtitle here'}
        </p>
      </div>

      {/* Description */}
      <div className="px-12 py-16 max-w-3xl mx-auto bg-white rounded-2xl shadow-xl">
        <p className="text-gray-700 text-lg leading-relaxed whitespace-pre-wrap text-center">
          {data.description || 'Your detailed description will appear here...'}
        </p>
      </div>

      {/* Features */}
      {data.features.length > 0 && (
        <div className="px-12 py-16">
          <h2 className="text-4xl font-serif font-bold text-blue-900 mb-12 text-center">
            Distinguished Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {data.features.map((feature, index) => (
              <div key={index} className="flex items-start gap-4 bg-white p-6 rounded-xl shadow-md">
                <div className="bg-amber-100 p-2 rounded-full flex-shrink-0">
                  <Check className="w-5 h-5 text-amber-700" />
                </div>
                <span className="text-gray-800">{feature || `Feature ${index + 1}`}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pricing */}
      <div className="px-12 py-20 text-center">
        <div className="inline-block bg-blue-900 text-white rounded-2xl px-16 py-12 shadow-2xl">
          <div className="text-amber-400 text-sm uppercase tracking-widest mb-4">Investment</div>
          <div className="flex items-baseline justify-center mb-2">
            <span className="text-3xl text-amber-400">{getCurrencySymbol(data.price.currency)}</span>
            <span className="text-7xl font-bold">{data.price.amount || 0}</span>
          </div>
          <div className="text-blue-200 mb-8">
            {data.price.interval === 'one-time' ? 'One-time investment' : `per ${data.price.interval}`}
          </div>
          <button className="bg-amber-600 text-white px-10 py-4 rounded-lg font-semibold hover:bg-amber-700 transition-colors">
            Reserve Your Spot
          </button>
        </div>
      </div>
    </div>
  )

  const renderVibrantTemplate = () => (
    <div className="bg-gradient-to-br from-purple-100 via-pink-100 to-yellow-100">
      {/* Header */}
      <div className="px-12 py-16 text-center">
        {data.logoUrl && (
          <img src={data.logoUrl} alt="Logo" className="h-12 mx-auto mb-8" />
        )}
        <h1 className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-yellow-600 mb-6">
          {data.title || 'Your Offer Title'}
        </h1>
        <p className="text-2xl text-gray-800 font-medium">
          {data.subtitle || 'Your subtitle here'}
        </p>
      </div>

      {/* Description */}
      <div className="px-12 py-12 max-w-4xl mx-auto">
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-10 shadow-xl">
          <p className="text-gray-700 text-lg leading-relaxed whitespace-pre-wrap">
            {data.description || 'Your detailed description will appear here...'}
          </p>
        </div>
      </div>

      {/* Features */}
      {data.features.length > 0 && (
        <div className="px-12 py-16">
          <h2 className="text-4xl font-black text-center mb-12 text-gray-900">
            ✨ Amazing Features ✨
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {data.features.map((feature, index) => (
              <div 
                key={index} 
                className="bg-white/90 backdrop-blur-sm p-6 rounded-2xl shadow-lg transform hover:scale-105 transition-transform"
              >
                <div className="flex items-start gap-3">
                  <div className="text-2xl">🎯</div>
                  <span className="text-gray-800 font-medium">{feature || `Feature ${index + 1}`}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pricing */}
      <div className="px-12 py-20 text-center">
        <div className="inline-block bg-gradient-to-r from-purple-600 via-pink-600 to-yellow-600 text-white rounded-3xl px-16 py-12 shadow-2xl transform hover:scale-105 transition-transform">
          <div className="text-sm uppercase tracking-wide mb-3 opacity-90">Special Price</div>
          <div className="flex items-baseline justify-center mb-3">
            <span className="text-3xl">{getCurrencySymbol(data.price.currency)}</span>
            <span className="text-7xl font-black">{data.price.amount || 0}</span>
          </div>
          <div className="text-sm mb-8 opacity-90">
            {data.price.interval === 'one-time' ? 'One-time only' : `per ${data.price.interval}`}
          </div>
          <button className="bg-white text-purple-600 px-12 py-4 rounded-2xl font-black text-xl hover:bg-gray-100 transition-colors">
            🚀 Get Started
          </button>
        </div>
      </div>
    </div>
  )

  const renderTemplate = () => {
    switch (data.template) {
      case 'bold':
        return renderBoldTemplate()
      case 'elegant':
        return renderElegantTemplate()
      case 'vibrant':
        return renderVibrantTemplate()
      default:
        return renderModernTemplate()
    }
  }

  return (
    <div className="w-3/5 bg-gray-100 overflow-hidden relative">
      {/* Preview Controls */}
      <div className="absolute top-4 right-4 z-10 flex gap-2">
        <button
          onClick={() => setZoom(zoom === 'fit' ? '100' : 'fit')}
          className="bg-white p-2 rounded-lg shadow-lg hover:bg-gray-50"
        >
          {zoom === 'fit' ? <Maximize2 className="w-5 h-5" /> : <Minimize2 className="w-5 h-5" />}
        </button>
      </div>

      {/* Preview Content */}
      <div className="h-screen overflow-y-auto p-8">
        <div className={`bg-white shadow-2xl ${zoom === 'fit' ? 'max-w-4xl' : 'w-full'} mx-auto`}>
          {renderTemplate()}
        </div>
      </div>
    </div>
  )
}
