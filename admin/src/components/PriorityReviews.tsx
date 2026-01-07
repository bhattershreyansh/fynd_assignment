import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { AdminReviewItem } from '../types/api';
import { AlertTriangle, Star, Calendar } from 'lucide-react';

export function PriorityReviews() {
  const [urgentReviews, setUrgentReviews] = useState<AdminReviewItem[]>([]);
  const [totalUrgent, setTotalUrgent] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPriorityReviews();
  }, []);

  const fetchPriorityReviews = async () => {
    try {
      const data = await api.getPriorityReviews(20);
      setUrgentReviews(data.urgent_reviews);
      setTotalUrgent(data.total_urgent);
    } catch (error) {
      console.error('Error fetching priority reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
        <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0" />
        <div>
          <p className="font-semibold text-red-900">
            {totalUrgent} {totalUrgent === 1 ? 'review' : 'reviews'} requiring immediate attention
          </p>
          <p className="text-sm text-red-700">
            These are 1-2 star reviews that may need follow-up action
          </p>
        </div>
      </div>

      {urgentReviews.length === 0 ? (
        <div className="text-center py-12 text-slate-600">
          No urgent reviews at this time
        </div>
      ) : (
        <div className="space-y-4">
          {urgentReviews.map((review) => (
            <UrgentReviewCard key={review.id} review={review} />
          ))}
        </div>
      )}
    </div>
  );
}

function UrgentReviewCard({ review }: { review: AdminReviewItem }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border-2 border-red-200 p-6 hover:shadow-md transition">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="bg-red-100 p-2 rounded-lg">
            <AlertTriangle className="w-5 h-5 text-red-600" />
          </div>
          <div className="flex items-center gap-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star
                key={i}
                className={`w-5 h-5 ${i < review.rating
                    ? 'fill-red-500 text-red-500'
                    : 'text-slate-300'
                  }`}
              />
            ))}
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-600">
          <Calendar className="w-4 h-4" />
          {new Date(review.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>

      <p className="text-slate-700 mb-4 leading-relaxed font-medium">
        {review.review_text}
      </p>

      {review.summary && (
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 mb-4">
          <p className="text-sm font-semibold text-slate-900 mb-2">Summary</p>
          <p className="text-sm text-slate-700">{review.summary}</p>
        </div>
      )}

      {review.recommended_actions && review.recommended_actions.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-red-900 mb-2">Recommended Actions</p>
          <ul className="space-y-2">
            {review.recommended_actions.map((action, idx) => (
              <li key={idx} className="text-sm text-red-800 flex items-start gap-2">
                <span className="text-red-600 font-bold">•</span>
                {action}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
