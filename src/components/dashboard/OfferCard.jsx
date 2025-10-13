import { Edit, Eye, Trash2 } from 'lucide-react'

export default function OfferCard({ offer, onEdit, onDelete }) {
  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getTemplateColor = (template) => {
    switch (template) {
      case 'modern':
        return 'bg-blue-100 text-blue-800'
      case 'bold':
        return 'bg-red-100 text-red-800'
      case 'elegant':
        return 'bg-purple-100 text-purple-800'
      case 'vibrant':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const editPercentage = ((offer.editCount || 0) / (offer.editLimit || 5)) * 100

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow overflow-hidden group">
      {/* Preview Image */}
      <div className="h-48 bg-gradient-to-br from-primary-100 to-purple-100 flex items-center justify-center relative overflow-hidden">
        <div className="text-center p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
            {offer.title || 'Untitled Offer'}
          </h3>
          <p className="text-sm text-gray-600 line-clamp-1">
            {offer.subtitle || 'No subtitle'}
          </p>
        </div>
        <div className="absolute top-3 right-3">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getTemplateColor(offer.template)}`}>
            {offer.template?.charAt(0).toUpperCase() + offer.template?.slice(1)}
          </span>
        </div>
      </div>

      {/* Card Content */}
      <div className="p-5">
        <div className="mb-4">
          <p className="text-sm text-gray-500 mb-1">
            Created: {formatDate(offer.createdAt || new Date())}
          </p>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">
              Edits: {offer.editCount || 0}/{offer.editLimit || 5}
            </span>
            <span className={`font-medium ${editPercentage > 80 ? 'text-red-600' : 'text-green-600'}`}>
              {Math.max(0, (offer.editLimit || 5) - (offer.editCount || 0))} left
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
            <div
              className={`h-1.5 rounded-full ${editPercentage > 80 ? 'bg-red-500' : 'bg-green-500'}`}
              style={{ width: `${Math.min(editPercentage, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(offer.id)}
            className="flex-1 bg-primary-600 text-white py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
          >
            <Edit className="w-4 h-4" />
            Edit
          </button>
          <button
            className="px-4 bg-gray-100 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            <Eye className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(offer.id)}
            className="px-4 bg-red-100 text-red-600 py-2 rounded-lg font-medium hover:bg-red-200 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
