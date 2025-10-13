import OfferCard from './OfferCard'
import { FileX, Plus } from 'lucide-react'

export default function OfferGrid({ offers, onEdit, onDelete, onCreate }) {
  if (offers.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-12 text-center">
        <div className="flex justify-center mb-6">
          <div className="bg-gray-100 p-6 rounded-full">
            <FileX className="w-16 h-16 text-gray-400" />
          </div>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          No offers yet
        </h3>
        <p className="text-gray-600 mb-6">
          Let's create your first stunning offer presentation!
        </p>
        <button
          onClick={onCreate}
          className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Your First Offer
        </button>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Offers</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {offers.map((offer) => (
          <OfferCard
            key={offer.id}
            offer={offer}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  )
}
