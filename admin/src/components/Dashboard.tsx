import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { Analytics } from '../types/api';
import { BarChart3, TrendingUp, Star, AlertCircle } from 'lucide-react';

export function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const data = await api.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900"></div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12 text-slate-600">
        Unable to load analytics data
      </div>
    );
  }

  const ratingPercentages = Object.entries(analytics.rating_distribution).map(
    ([rating, count]) => ({
      rating: parseInt(rating),
      count,
      percentage: analytics.total_reviews > 0
        ? (count / analytics.total_reviews) * 100
        : 0,
    })
  ).reverse();

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<BarChart3 className="w-6 h-6" />}
          label="Total Reviews"
          value={analytics.total_reviews.toLocaleString()}
          color="bg-blue-500"
        />
        <StatCard
          icon={<Star className="w-6 h-6" />}
          label="Average Rating"
          value={analytics.average_rating.toFixed(2)}
          color="bg-amber-500"
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6" />}
          label="Recent (24h)"
          value={analytics.recent_reviews_count.toLocaleString()}
          color="bg-green-500"
        />
        <StatCard
          icon={<AlertCircle className="w-6 h-6" />}
          label="Urgent Reviews"
          value={(analytics.rating_distribution[1] + analytics.rating_distribution[2]).toLocaleString()}
          color="bg-red-500"
        />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-6">Rating Distribution</h2>
        <div className="space-y-4">
          {ratingPercentages.map(({ rating, count, percentage }) => (
            <div key={rating} className="flex items-center gap-4">
              <div className="flex items-center gap-1 w-20">
                <span className="font-medium text-slate-700">{rating}</span>
                <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
              </div>
              <div className="flex-1">
                <div className="bg-slate-100 rounded-full h-8 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-amber-400 to-amber-500 h-full flex items-center justify-end px-3 transition-all duration-500"
                    style={{ width: `${Math.max(percentage, 2)}%` }}
                  >
                    {count > 0 && (
                      <span className="text-xs font-semibold text-white">
                        {count}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <div className="w-16 text-right text-sm font-medium text-slate-600">
                {percentage.toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: string;
}

function StatCard({ icon, label, value, color }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-4">
        <div className={`${color} p-3 rounded-lg text-white`}>
          {icon}
        </div>
        <div>
          <p className="text-sm text-slate-600 mb-1">{label}</p>
          <p className="text-2xl font-bold text-slate-900">{value}</p>
        </div>
      </div>
    </div>
  );
}
