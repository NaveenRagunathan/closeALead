import { motion } from 'framer-motion'
import { Bot, Palette, Layout, Zap, BarChart, FileDown } from 'lucide-react'

const features = [
  {
    icon: Bot,
    title: 'AI-Powered Design',
    description: 'ChatGPT for offer creation. Just describe, we design. No design skills needed.',
    color: 'text-blue-600',
    bgColor: 'bg-blue-100'
  },
  {
    icon: Palette,
    title: 'Brand Consistency',
    description: 'Your colors, your logo, your identity - perfectly matched across every offer.',
    color: 'text-purple-600',
    bgColor: 'bg-purple-100'
  },
  {
    icon: Layout,
    title: 'Template Library',
    description: '4 conversion-tested templates that actually close deals. Choose your style.',
    color: 'text-pink-600',
    bgColor: 'bg-pink-100'
  },
  {
    icon: Zap,
    title: 'Instant Redesigns',
    description: 'Paste your old offer, get a stunning upgrade in seconds. Transform instantly.',
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100'
  },
  {
    icon: BarChart,
    title: 'Edit Tracking',
    description: 'Know exactly where you stand with your plan limits. Full transparency.',
    color: 'text-green-600',
    bgColor: 'bg-green-100'
  },
  {
    icon: FileDown,
    title: 'Export Ready',
    description: 'PDF-quality presentations that impress every time. Download and send.',
    color: 'text-red-600',
    bgColor: 'bg-red-100'
  }
]

export default function Features() {
  return (
    <section id="features" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Everything You Need to Close More Deals
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to transform your offers into conversion machines
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100"
            >
              <div className={`w-14 h-14 ${feature.bgColor} rounded-xl flex items-center justify-center mb-4`}>
                <feature.icon className={`w-7 h-7 ${feature.color}`} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
