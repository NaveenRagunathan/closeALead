import { useState } from 'react'
import { Menu, X } from 'lucide-react'

export default function Navigation({ onLoginClick, onSignupClick }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <nav className="sticky top-0 bg-white/80 backdrop-blur-md z-40 border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="text-2xl font-bold text-primary-600">
              CloseALead
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-700 hover:text-primary-600 transition-colors">
              Features
            </a>
            <a href="#pricing" className="text-gray-700 hover:text-primary-600 transition-colors">
              Pricing
            </a>
            <a href="#examples" className="text-gray-700 hover:text-primary-600 transition-colors">
              Examples
            </a>
            <button
              onClick={onLoginClick}
              className="text-gray-700 hover:text-primary-600 transition-colors"
            >
              Login
            </button>
            <button
              onClick={onSignupClick}
              className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Get Started Free
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-gray-700"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-4 py-4 space-y-4">
            <a href="#features" className="block text-gray-700 hover:text-primary-600">
              Features
            </a>
            <a href="#pricing" className="block text-gray-700 hover:text-primary-600">
              Pricing
            </a>
            <a href="#examples" className="block text-gray-700 hover:text-primary-600">
              Examples
            </a>
            <button
              onClick={onLoginClick}
              className="block w-full text-left text-gray-700 hover:text-primary-600"
            >
              Login
            </button>
            <button
              onClick={onSignupClick}
              className="block w-full bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700"
            >
              Get Started Free
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}
