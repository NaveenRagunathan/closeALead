import { Sparkles, Upload } from 'lucide-react'

export default function ModeSelector({ onSelect }) {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">
        How would you like to create your offer?
      </h2>
      <p className="text-gray-600 mb-12 text-lg">
        Choose the method that works best for you
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Create From Scratch */}
        <button
          onClick={() => onSelect('scratch')}
          className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all border-2 border-transparent hover:border-primary-600 text-left"
        >
          <div className="bg-primary-100 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Sparkles className="w-8 h-8 text-primary-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-3">
            Create From Scratch
          </h3>
          <p className="text-gray-600 mb-4">
            Describe your offer and let AI design everything from the ground up
          </p>
          <div className="text-primary-600 font-medium group-hover:translate-x-2 transition-transform inline-block">
            Get Started →
          </div>
        </button>

        {/* Redesign Existing */}
        <button
          onClick={() => onSelect('redesign')}
          className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all border-2 border-transparent hover:border-purple-600 text-left"
        >
          <div className="bg-purple-100 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Upload className="w-8 h-8 text-purple-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-3">
            Redesign Existing
          </h3>
          <p className="text-gray-600 mb-4">
            Upload your current offer and get it professionally redesigned
          </p>
          <div className="text-purple-600 font-medium group-hover:translate-x-2 transition-transform inline-block">
            Upload Offer →
          </div>
        </button>
      </div>
    </div>
  )
}
