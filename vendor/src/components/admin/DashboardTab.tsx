import { useEffect, useState } from 'react';
import { Star, TrendingUp, MessageSquare, Clock } from 'lucide-react';
import { api, AnalyticsResponse } from '../../services/api';

export default function DashboardTab() {
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const data = await api.getAnalytics();
      setAnalytics(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={loadAnalytics}
          className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!analytics) {
    return null;
  }

  const maxCount = Math.max(...Object.values(analytics.rating_distribution));

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-600 text-sm font-medium">Total Reviews</h3>
            <MessageSquare className="w-5 h-5 text-blue-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">{analytics.total_reviews}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-600 text-sm font-medium">Average Rating</h3>
            <Star className="w-5 h-5 text-yellow-500" />
          </div>
          <p className="text-3xl font-bold text-gray-900">{analytics.average_rating.toFixed(2)}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-600 text-sm font-medium">Recent Reviews</h3>
            <Clock className="w-5 h-5 text-green-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">{analytics.recent_reviews_count}</p>
          <p className="text-xs text-gray-500 mt-1">Last 24 hours</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-gray-600 text-sm font-medium">Trend</h3>
            <TrendingUp className="w-5 h-5 text-purple-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {analytics.recent_reviews_count > 0 ? '+' : ''}
            {analytics.recent_reviews_count}
          </p>
          <p className="text-xs text-gray-500 mt-1">Today</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Rating Distribution</h3>

        <div className="space-y-4">
          {[5, 4, 3, 2, 1].map((rating) => {
            const count = analytics.rating_distribution[rating] || 0;
            const percentage = analytics.total_reviews > 0
              ? (count / analytics.total_reviews) * 100
              : 0;
            const barWidth = maxCount > 0 ? (count / maxCount) * 100 : 0;

            return (
              <div key={rating} className="flex items-center gap-4">
                <div className="flex items-center gap-1 w-20">
                  <span className="font-medium text-gray-700">{rating}</span>
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                </div>

                <div className="flex-1 bg-gray-200 rounded-full h-8 relative overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${barWidth}%` }}
                  />
                  <div className="absolute inset-0 flex items-center px-3">
                    <span className="text-sm font-medium text-gray-700">
                      {count} reviews
                    </span>
                  </div>
                </div>

                <div className="w-16 text-right">
                  <span className="text-sm font-medium text-gray-600">
                    {percentage.toFixed(1)}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
