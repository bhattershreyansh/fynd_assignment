import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { AdminReviewItem } from '../types/api';
import { Star, Calendar, ChevronLeft, ChevronRight, Filter, Download } from 'lucide-react';

export function ReviewsList() {
  const [reviews, setReviews] = useState<AdminReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [ratingFilter, setRatingFilter] = useState<number | null>(null);
  const pageSize = 20;

  useEffect(() => {
    fetchReviews();
  }, [page, ratingFilter]);

  const fetchReviews = async () => {
    setLoading(true);
    try {
      const data = await api.getReviews(page, pageSize, ratingFilter || undefined);
      setReviews(data.reviews);
      setTotal(data.total);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const blob = await api.exportReviews(ratingFilter || undefined);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reviews_export_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting reviews:', error);
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-slate-600" />
          <select
            value={ratingFilter || ''}
            onChange={(e) => {
              setRatingFilter(e.target.value ? parseInt(e.target.value) : null);
              setPage(1);
            }}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
          >
            <option value="">All Ratings</option>
            {[5, 4, 3, 2, 1].map(rating => (
              <option key={rating} value={rating}>
                {rating} Star{rating !== 1 ? 's' : ''}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900"></div>
        </div>
      ) : reviews.length === 0 ? (
        <div className="text-center py-12 text-slate-600">
          No reviews found
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {reviews.map((review) => (
              <ReviewCard key={review.id} review={review} />
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-600">
                Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} reviews
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
                <span className="px-4 py-2 border border-slate-300 rounded-lg bg-slate-50">
                  {page} / {totalPages}
                </span>
                <button
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function ReviewCard({ review }: { review: AdminReviewItem }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <Star
              key={i}
              className={`w-5 h-5 ${i < review.rating
                  ? 'fill-amber-400 text-amber-400'
                  : 'text-slate-300'
                }`}
            />
          ))}
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-600">
          <Calendar className="w-4 h-4" />
          {new Date(review.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          })}
        </div>
      </div>

      <p className="text-slate-700 mb-4 leading-relaxed">{review.review_text}</p>

      {review.summary && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <p className="text-sm font-semibold text-blue-900 mb-2">Summary</p>
          <p className="text-sm text-blue-800">{review.summary}</p>
        </div>
      )}

      {review.recommended_actions && review.recommended_actions.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-amber-900 mb-2">Recommended Actions</p>
          <ul className="space-y-1">
            {review.recommended_actions.map((action, idx) => (
              <li key={idx} className="text-sm text-amber-800 flex items-start gap-2">
                <span className="text-amber-600">•</span>
                {action}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
