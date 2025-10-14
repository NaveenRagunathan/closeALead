import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check } from 'lucide-react'

const plans = {
  free: {
    name: 'Free',
    monthlyPrice: 0,
    annualPrice: 0,
    features: [
      '1 active offer at a time',
      '5 total edits per offer',
      'All 4 templates',
      'AI assistance',
      'Email support',
      'PDF export'
    ],
    cta: 'Start Free',
    popular: false
  },
  professional: {
    name: 'Professional',
    monthlyPrice: 12,
    annualPrice: 8.75,
    annualTotal: 105,
    features: [
      '4 simultaneous offers',
      '15 edits per offer',
      'Priority AI processing',
      'Custom branding',
      'Client personalization',
      'Priority support',
      'Advanced templates',
      'Analytics dashboard'
    ],
    cta: 'Go Professional',
    popular: true
  },
  agency: {
    name: 'Agency',
    monthlyPrice: 35,
    annualPrice: 24.58,
    annualTotal: 295,
    features: [
      'Unlimited offers',
      'Unlimited edits',
      'White-label options',
      'API access',
      'Team collaboration',
      'Dedicated success manager',
      'Custom integrations',
      'SLA guarantee'
    ],
    cta: 'Scale Your Agency',
    popular: false
  }
}

export default function Pricing({ onSelectPlan }) {
  const [billingInterval, setBillingInterval] = useState('monthly')

  return (
    <section id="pricing" className="py-24 bg-gradient-to-br from-gray-50 to-primary-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Choose the plan that fits your needs. Upgrade or downgrade anytime.
            </p>

            {/* Billing Toggle */}
            <div className="inline-flex items-center bg-white rounded-full p-1 shadow-lg">
              <button
                onClick={() => setBillingInterval('monthly')}
                className={`px-6 py-2 rounded-full font-medium transition-colors ${
                  billingInterval === 'monthly'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBillingInterval('annual')}
                className={`px-6 py-2 rounded-full font-medium transition-colors ${
                  billingInterval === 'annual'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Annual
                <span className="ml-2 text-xs bg-green-500 text-white px-2 py-1 rounded-full">
                  Save 10%
                </span>
              </button>
            </div>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {Object.entries(plans).map(([key, plan], index) => (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className={`relative bg-white rounded-2xl shadow-xl p-8 ${
                plan.popular ? 'ring-4 ring-primary-600 transform scale-105' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {plan.name}
                </h3>
                <div className="flex items-baseline justify-center">
                  <span className="text-5xl font-bold text-gray-900">
                    ${billingInterval === 'monthly' ? plan.monthlyPrice : plan.annualPrice}
                  </span>
                  <span className="text-gray-600 ml-2">/month</span>
                </div>
                {billingInterval === 'annual' && plan.annualPrice > 0 && (
                  <p className="text-sm text-gray-500 mt-2">
                    Billed annually (${plan.annualTotal}/year)
                  </p>
                )}
              </div>

              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <Check className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-600">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => onSelectPlan(key)}
                className={`w-full py-3 rounded-lg font-semibold transition-colors ${
                  plan.popular
                    ? 'bg-primary-600 text-white hover:bg-primary-700'
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}
              >
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
