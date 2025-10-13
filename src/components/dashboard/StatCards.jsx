import { FileText, Crown, Edit } from 'lucide-react'

const PLAN_LIMITS = {
  free: { offers: 1, editsPerOffer: 5 },
  professional: { offers: 4, editsPerOffer: 15 },
  enterprise: { offers: Infinity, editsPerOffer: Infinity }
}

export default function StatCards({ user, offers }) {
  const planLimits = PLAN_LIMITS[user?.plan || 'free']
  const totalOffers = offers.length
  const offerUtilization = (totalOffers / planLimits.offers) * 100

  const totalEditsRemaining = offers.reduce((sum, offer) => {
    const used = offer.editCount || 0
    const limit = planLimits.editsPerOffer
    return sum + Math.max(0, limit - used)
  }, 0)

  const getPlanColor = (plan) => {
    switch (plan) {
      case 'free':
        return 'bg-gray-100 text-gray-800'
      case 'professional':
        return 'bg-blue-100 text-blue-800'
      case 'enterprise':
        return 'bg-purple-100 text-purple-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Total Offers */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="bg-primary-100 p-3 rounded-lg">
            <FileText className="w-6 h-6 text-primary-600" />
          </div>
        </div>
        <div className="text-3xl font-bold text-gray-900 mb-1">
          {totalOffers}
          {planLimits.offers !== Infinity && (
            <span className="text-lg text-gray-500"> / {planLimits.offers}</span>
          )}
        </div>
        <p className="text-gray-600 mb-3">Total Offers</p>
        {planLimits.offers !== Infinity && (
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${
                offerUtilization > 80 ? 'bg-red-500' : 'bg-primary-600'
              }`}
              style={{ width: `${Math.min(offerUtilization, 100)}%` }}
            ></div>
          </div>
        )}
      </div>

      {/* Current Plan */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="bg-purple-100 p-3 rounded-lg">
            <Crown className="w-6 h-6 text-purple-600" />
          </div>
        </div>
        <div className="mb-3">
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getPlanColor(user?.plan)}`}>
            {user?.plan?.charAt(0).toUpperCase() + user?.plan?.slice(1)}
          </span>
        </div>
        <p className="text-gray-600 mb-3">Current Plan</p>
        {user?.plan !== 'enterprise' && (
          <button className="text-primary-600 hover:text-primary-700 font-medium text-sm">
            Upgrade Plan →
          </button>
        )}
      </div>

      {/* Edits Remaining */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="bg-green-100 p-3 rounded-lg">
            <Edit className="w-6 h-6 text-green-600" />
          </div>
        </div>
        <div className="text-3xl font-bold text-gray-900 mb-1">
          {planLimits.editsPerOffer === Infinity ? '∞' : totalEditsRemaining}
        </div>
        <p className="text-gray-600 mb-3">Edits Remaining</p>
        {totalEditsRemaining < 10 && planLimits.editsPerOffer !== Infinity && (
          <p className="text-yellow-600 text-sm">⚠️ Running low on edits</p>
        )}
      </div>
    </div>
  )
}
