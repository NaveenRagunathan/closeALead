import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User } from 'lucide-react'

const CONVERSATION_FLOW = [
  {
    question: "Hi! I'm here to help create your stunning offer. What service or product are you offering?",
    field: 'service_name'
  },
  {
    question: "Great! Who is your ideal customer? Be as specific as possible.",
    field: 'target_audience'
  },
  {
    question: "What's the main problem or pain point this solves for them?",
    field: 'problem_solved'
  },
  {
    question: "Perfect! What's your price point?",
    field: 'pricing'
  },
  {
    question: "What are the key features or deliverables? (List at least 3)",
    field: 'features'
  },
  {
    question: "What makes your offer unique or different from competitors?",
    field: 'unique_value'
  },
  {
    question: "Do you offer any guarantees or bonuses?",
    field: 'guarantees'
  },
  {
    question: "Finally, how would you describe your brand personality? (professional, friendly, bold, luxurious)",
    field: 'brand_personality'
  }
]

export default function AIChat({ onComplete }) {
  const [messages, setMessages] = useState([
    { role: 'ai', content: CONVERSATION_FLOW[0].question }
  ])
  const [currentInput, setCurrentInput] = useState('')
  const [currentStep, setCurrentStep] = useState(0)
  const [collectedData, setCollectedData] = useState({})
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!currentInput.trim()) return

    // Add user message
    const userMessage = { role: 'user', content: currentInput }
    setMessages([...messages, userMessage])

    // Store the answer
    const currentQuestion = CONVERSATION_FLOW[currentStep]
    const updatedData = { ...collectedData, [currentQuestion.field]: currentInput }
    setCollectedData(updatedData)

    setCurrentInput('')

    // Move to next question or complete
    if (currentStep < CONVERSATION_FLOW.length - 1) {
      setTimeout(() => {
        const nextQuestion = CONVERSATION_FLOW[currentStep + 1]
        setMessages(prev => [...prev, { role: 'ai', content: nextQuestion.question }])
        setCurrentStep(currentStep + 1)
      }, 500)
    } else {
      // All questions answered, process with AI
      setIsProcessing(true)
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: 'ai', 
          content: 'Perfect! I have all the information I need. Let me create your stunning offer...' 
        }])
      }, 500)

      // Simulate AI processing
      setTimeout(() => {
        const processedOffer = processOfferData(updatedData)
        onComplete(processedOffer)
      }, 2000)
    }
  }

  const processOfferData = (data) => {
    // This would normally call the CrewAI backend
    // For MVP, we'll do basic processing
    return {
      title: `${data.service_name || 'Professional Service'}`,
      subtitle: `Transform Your Business with ${data.service_name}`,
      description: `Are you struggling with ${data.problem_solved}? We help ${data.target_audience} achieve their goals through our proven ${data.service_name}. ${data.unique_value}`,
      price: {
        amount: parseInt(data.pricing) || 997,
        currency: 'USD',
        interval: 'one-time'
      },
      features: data.features?.split('\n').filter(f => f.trim()) || [
        'Feature 1',
        'Feature 2',
        'Feature 3'
      ],
      template: data.brand_personality === 'bold' ? 'bold' :
                data.brand_personality === 'elegant' ? 'elegant' :
                data.brand_personality === 'luxurious' ? 'elegant' : 'modern'
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
      {/* Chat Header */}
      <div className="bg-primary-600 text-white p-4">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-lg">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-semibold">CloseALead AI Assistant</h3>
            <p className="text-sm text-primary-100">
              Step {currentStep + 1} of {CONVERSATION_FLOW.length}
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="h-96 overflow-y-auto p-6 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {message.role === 'ai' && (
              <div className="bg-primary-100 p-2 rounded-lg h-fit">
                <Bot className="w-5 h-5 text-primary-600" />
              </div>
            )}
            <div
              className={`max-w-md p-4 rounded-xl ${
                message.role === 'ai'
                  ? 'bg-gray-100 text-gray-900'
                  : 'bg-primary-600 text-white'
              }`}
            >
              {message.content}
            </div>
            {message.role === 'user' && (
              <div className="bg-primary-100 p-2 rounded-lg h-fit">
                <User className="w-5 h-5 text-primary-600" />
              </div>
            )}
          </div>
        ))}
        {isProcessing && (
          <div className="flex justify-center">
            <div className="animate-pulse text-gray-500">Processing your offer...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      {!isProcessing && (
        <form onSubmit={handleSubmit} className="border-t p-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={currentInput}
              onChange={(e) => setCurrentInput(e.target.value)}
              placeholder="Type your answer..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              autoFocus
            />
            <button
              type="submit"
              disabled={!currentInput.trim()}
              className="bg-primary-600 text-white p-3 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
