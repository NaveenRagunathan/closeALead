import { Check } from 'lucide-react'

const templates = [
  {
    id: 'modern',
    name: 'Modern',
    description: 'Clean, minimalist design with lots of whitespace',
    colors: ['#3b82f6', '#6b7280', '#f3f4f6'],
    bestFor: 'Tech, SaaS, consulting'
  },
  {
    id: 'bold',
    name: 'Bold',
    description: 'High contrast, statement-making design',
    colors: ['#000000', '#ef4444', '#ffffff'],
    bestFor: 'Creative agencies, coaching'
  },
  {
    id: 'elegant',
    name: 'Elegant',
    description: 'Sophisticated and luxurious',
    colors: ['#1e3a8a', '#d97706', '#fef3c7'],
    bestFor: 'Premium services, legal, finance'
  },
  {
    id: 'vibrant',
    name: 'Vibrant',
    description: 'Energetic and colorful',
    colors: ['#8b5cf6', '#ec4899', '#f59e0b'],
    bestFor: 'Marketing, events, creative'
  }
]

export default function TemplateSelector({ selectedTemplate, onSelect }) {
  return (
    <div>
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Choose Your Template Style
        </h2>
        <p className="text-gray-600 text-lg">
          Select a template that matches your brand personality
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {templates.map((template) => (
          <button
            key={template.id}
            onClick={() => onSelect(template.id)}
            className={`group bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all p-6 text-left ${
              selectedTemplate === template.id
                ? 'ring-4 ring-primary-600'
                : ''
            }`}
          >
            {/* Template Preview */}
            <div className="relative h-48 rounded-lg mb-4 overflow-hidden flex items-center justify-center"
              style={{ background: `linear-gradient(135deg, ${template.colors[0]}, ${template.colors[1]})` }}
            >
              <div className="text-white text-center">
                <div className="text-2xl font-bold mb-2">{template.name}</div>
                <div className="text-sm opacity-80">Preview</div>
              </div>
              {selectedTemplate === template.id && (
                <div className="absolute top-3 right-3 bg-white rounded-full p-1">
                  <Check className="w-5 h-5 text-primary-600" />
                </div>
              )}
            </div>

            {/* Template Info */}
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              {template.name}
            </h3>
            <p className="text-gray-600 text-sm mb-3">
              {template.description}
            </p>

            {/* Color Palette */}
            <div className="flex gap-2 mb-3">
              {template.colors.map((color, index) => (
                <div
                  key={index}
                  className="w-8 h-8 rounded-full border-2 border-gray-200"
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>

            <p className="text-xs text-gray-500">
              Best for: {template.bestFor}
            </p>
          </button>
        ))}
      </div>

      <div className="text-center mt-8">
        <button
          onClick={() => onSelect(selectedTemplate)}
          className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
        >
          Continue with {templates.find(t => t.id === selectedTemplate)?.name || 'Selected'} Template
        </button>
      </div>
    </div>
  )
}
