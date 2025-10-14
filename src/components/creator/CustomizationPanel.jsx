import { useState } from 'react'
import { Type, DollarSign, List, Palette, Image as ImageIcon } from 'lucide-react'

export default function CustomizationPanel({ data, onChange }) {
  const [activeSection, setActiveSection] = useState('content')

  const sections = [
    { id: 'content', label: 'Content', icon: Type },
    { id: 'pricing', label: 'Pricing', icon: DollarSign },
    { id: 'features', label: 'Features', icon: List },
    { id: 'branding', label: 'Branding', icon: Palette },
    { id: 'images', label: 'Images', icon: ImageIcon }
  ]

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...data.features]
    newFeatures[index] = value
    onChange('features', newFeatures)
  }

  const addFeature = () => {
    if (data.features.length < 10) {
      onChange('features', [...data.features, ''])
    }
  }

  const removeFeature = (index) => {
    const newFeatures = data.features.filter((_, i) => i !== index)
    onChange('features', newFeatures)
  }

  return (
    <div className="w-2/5 bg-white border-r border-gray-200 overflow-y-auto h-screen">
      {/* Section Tabs */}
      <div className="border-b border-gray-200 bg-gray-50 p-4">
        <div className="flex gap-2 overflow-x-auto">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
                activeSection === section.id
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              <section.icon className="w-4 h-4" />
              {section.label}
            </button>
          ))}
        </div>
      </div>

      <div className="p-6">
        {/* Content Section */}
        {activeSection === 'content' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Client Name <span className="text-gray-500">(Optional - Personalize)</span>
              </label>
              <input
                type="text"
                value={data.clientName || ''}
                onChange={(e) => onChange('clientName', e.target.value.slice(0, 100))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="e.g., John Smith or Acme Corp"
              />
              <p className="text-xs text-gray-500 mt-1">
                Add your client's name to personalize the offer for them
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title <span className="text-gray-500">({data.title.length}/60)</span>
              </label>
              <input
                type="text"
                value={data.title}
                onChange={(e) => onChange('title', e.target.value.slice(0, 60))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Your Offer Title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Subtitle <span className="text-gray-500">({data.subtitle.length}/120)</span>
              </label>
              <textarea
                value={data.subtitle}
                onChange={(e) => onChange('subtitle', e.target.value.slice(0, 120))}
                rows="2"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Brief description of your offer"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description <span className="text-gray-500">({data.description.split(' ').length} words)</span>
              </label>
              <textarea
                value={data.description}
                onChange={(e) => onChange('description', e.target.value)}
                rows="8"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Detailed description of your offer..."
              />
            </div>
          </div>
        )}

        {/* Pricing Section */}
        {activeSection === 'pricing' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Price Amount
              </label>
              <input
                type="number"
                value={data.price.amount}
                onChange={(e) => onChange('price', { ...data.price, amount: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Currency
              </label>
              <select
                value={data.price.currency}
                onChange={(e) => onChange('price', { ...data.price, currency: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="CAD">CAD ($)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Billing Interval
              </label>
              <div className="space-y-2">
                {['one-time', 'monthly', 'annually'].map((interval) => (
                  <label key={interval} className="flex items-center">
                    <input
                      type="radio"
                      value={interval}
                      checked={data.price.interval === interval}
                      onChange={(e) => onChange('price', { ...data.price, interval: e.target.value })}
                      className="mr-2"
                    />
                    <span className="capitalize">{interval.replace('-', ' ')}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Features Section */}
        {activeSection === 'features' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <label className="block text-sm font-medium text-gray-700">
                Features ({data.features.length}/10)
              </label>
              <button
                onClick={addFeature}
                disabled={data.features.length >= 10}
                className="text-primary-600 hover:text-primary-700 font-medium text-sm disabled:opacity-50"
              >
                + Add Feature
              </button>
            </div>

            {data.features.map((feature, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={feature}
                  onChange={(e) => handleFeatureChange(index, e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder={`Feature ${index + 1}`}
                />
                <button
                  onClick={() => removeFeature(index)}
                  className="px-3 text-red-600 hover:text-red-700"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Branding Section */}
        {activeSection === 'branding' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Logo URL
              </label>
              <input
                type="text"
                value={data.logoUrl}
                onChange={(e) => onChange('logoUrl', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="https://example.com/logo.png"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Brand Colors
              </label>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Primary Color</label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={data.brandColors.primary}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, primary: e.target.value })}
                      className="w-12 h-12 rounded cursor-pointer"
                    />
                    <input
                      type="text"
                      value={data.brandColors.primary}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, primary: e.target.value })}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs text-gray-600 mb-1">Secondary Color</label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={data.brandColors.secondary}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, secondary: e.target.value })}
                      className="w-12 h-12 rounded cursor-pointer"
                    />
                    <input
                      type="text"
                      value={data.brandColors.secondary}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, secondary: e.target.value })}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs text-gray-600 mb-1">Accent Color</label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={data.brandColors.accent}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, accent: e.target.value })}
                      className="w-12 h-12 rounded cursor-pointer"
                    />
                    <input
                      type="text"
                      value={data.brandColors.accent}
                      onChange={(e) => onChange('brandColors', { ...data.brandColors, accent: e.target.value })}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Images Section */}
        {activeSection === 'images' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hero Image URL
              </label>
              <input
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="https://example.com/hero.jpg"
              />
            </div>

            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <ImageIcon className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600 mb-2">Upload images</p>
              <button className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                Browse Files
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
