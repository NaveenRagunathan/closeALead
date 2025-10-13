import { useState } from 'react'
import Navigation from '../components/landing/Navigation'
import Hero from '../components/landing/Hero'
import Features from '../components/landing/Features'
import Pricing from '../components/landing/Pricing'
import SignUpModal from '../components/auth/SignUpModal'
import LoginModal from '../components/auth/LoginModal'

export default function LandingPage() {
  const [showSignup, setShowSignup] = useState(false)
  const [showLogin, setShowLogin] = useState(false)

  return (
    <div className="min-h-screen">
      <Navigation
        onLoginClick={() => setShowLogin(true)}
        onSignupClick={() => setShowSignup(true)}
      />
      <Hero onGetStarted={() => setShowSignup(true)} />
      <Features />
      <Pricing onSelectPlan={() => setShowSignup(true)} />

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="text-2xl font-bold mb-4">CloseALead</div>
            <p className="text-gray-400 mb-4">
              Transform your offers into irresistible presentations
            </p>
            <p className="text-gray-500 text-sm">
              © 2025 CloseALead. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      <SignUpModal
        isOpen={showSignup}
        onClose={() => setShowSignup(false)}
        onSwitchToLogin={() => {
          setShowSignup(false)
          setShowLogin(true)
        }}
      />
      <LoginModal
        isOpen={showLogin}
        onClose={() => setShowLogin(false)}
        onSwitchToSignup={() => {
          setShowLogin(false)
          setShowSignup(true)
        }}
      />
    </div>
  )
}
