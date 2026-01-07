import { useEffect, useState } from 'react';
import { Star, AlertTriangle } from 'lucide-react';
import { api, AdminReviewItem } from '../../services/api';

export default function PriorityReviewsTab() {
  const [reviews, setReviews] = useState<AdminReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalUrgent, setTotalUrgent] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadPriorityReviews();
    const interval = setInterval(loadPriorityReviews, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadPriorityReviews = async () => {
    try {
      setLoading(true);
      const data = await api.getPriorityReviews(50);
      setReviews(data.urgent_reviews);
      setTotalUrgent(data.total_urgent);
      setMessage(data.message);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load priority reviews');
    } finally {
      setLoading(false);
    }
  };

  if (loading && reviews.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Priority Reviews</h2>
          <p className="text-gray-600">{message}</p>
        </div>

        <div className="bg-red-100 border border-red-300 rounded-lg px-4 py-2">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            <span className="font-bold text-red-900">{totalUrgent} Urgent</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {reviews.length === 0 && !loading ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <AlertTriangle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Priority Reviews</h3>
          <p className="text-gray-600">All reviews are currently in good standing</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow divide-y divide-gray-200">
          {reviews.map((review) => (
            <div key={review.id} className="p-6 hover:bg-red-50 transition-colors border-l-4 border-red-500">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        className={`w-5 h-5 ${
                          star <= review.rating
                            ? 'text-red-500 fill-red-500'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="font-semibold text-red-900">{review.rating}/5</span>
                  <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-semibold rounded">
                    URGENT
                  </span>
                </div>
                <span className="text-sm text-gray-500">
                  {new Date(review.created_at).toLocaleString()}
                </span>
              </div>

              <div className="mb-4">
                <h4 className="font-semibold text-gray-900 mb-2">Review:</h4>
                <p className="text-gray-700">{review.review_text}</p>
              </div>

              {review.summary && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <h4 className="font-semibold text-red-900 mb-2">AI Summary:</h4>
                  <p className="text-red-800">{review.summary}</p>
                </div>
              )}

              {review.recommended_actions && review.recommended_actions.length > 0 && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <h4 className="font-semibold text-yellow-900 mb-2">Immediate Actions Required:</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {review.recommended_actions.map((action, idx) => (
                      <li key={idx} className="text-yellow-800 font-medium">{action}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
