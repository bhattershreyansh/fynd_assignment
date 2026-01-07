import { useState } from 'react';
import { Star, MessageSquare, Send, CheckCircle, AlertCircle } from 'lucide-react';
import { api, ReviewSubmitResponse } from '../services/api';

export default function UserDashboard() {
  const [name, setName] = useState('');
  const [rating, setRating] = useState<number>(0);
  const [hoveredRating, setHoveredRating] = useState<number>(0);
  const [reviewText, setReviewText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResponse, setSubmitResponse] = useState<ReviewSubmitResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) {
      setError('Please enter your name');
      return;
    }

    if (rating === 0) {
      setError('Please select a rating');
      return;
    }

    if (reviewText.trim().length < 10) {
      setError('Review must be at least 10 characters');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await api.submitReview({
        name: name.trim(),
        rating,
        review_text: reviewText,
      });

      setSubmitResponse(response);
      setName('');
      setRating(0);
      setReviewText('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit review');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewReview = () => {
    setSubmitResponse(null);
    setError(null);
  };

  if (submitResponse) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-gray-800 rounded-lg shadow-xl p-8">
          <div className="text-center mb-6">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">Thank You for Your Feedback!</h2>
          </div>

          <div className="bg-gray-700 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Thank You for Your Feedback</h3>
            <p className="text-gray-300 leading-relaxed">{submitResponse.user_response}</p>
          </div>

          <div className="flex items-center justify-between text-sm text-gray-400 mb-6">
            <span>Rating: {submitResponse.rating} ⭐</span>
            <span>Submitted: {new Date(submitResponse.created_at).toLocaleString()}</span>
          </div>

          <button
            onClick={handleNewReview}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg transition-colors"
          >
            Submit Another Review
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <MessageSquare className="w-16 h-16 text-blue-500 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-white mb-2">Share Your Experience</h1>
          <p className="text-gray-400">We value your feedback and want to hear from you</p>
        </div>

        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2 text-lg">
                Your Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                className="w-full bg-gray-700 text-white rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                maxLength={50}
              />
            </div>

            <div className="mb-8">
              <label className="block text-white font-semibold mb-4 text-lg">
                How would you rate your experience?
              </label>
              <div className="flex justify-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(0)}
                    className="transition-transform hover:scale-110 focus:outline-none"
                  >
                    <Star
                      className={`w-12 h-12 ${star <= (hoveredRating || rating)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-gray-600'
                        }`}
                    />
                  </button>
                ))}
              </div>
              {rating > 0 && (
                <p className="text-center text-gray-400 mt-2">
                  {rating === 1 && 'Poor'}
                  {rating === 2 && 'Fair'}
                  {rating === 3 && 'Good'}
                  {rating === 4 && 'Very Good'}
                  {rating === 5 && 'Excellent'}
                </p>
              )}
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2 text-lg">
                Tell us more about your experience
              </label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Share your thoughts... (minimum 10 characters)"
                className="w-full bg-gray-700 text-white rounded-lg p-4 min-h-[150px] focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                maxLength={5000}
              />
              <div className="flex justify-between text-sm text-gray-400 mt-2">
                <span>{reviewText.length}/5000 characters</span>
                <span>{reviewText.length >= 10 ? '✓' : ''} Min 10 characters</span>
              </div>
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-900/50 border border-red-500 rounded-lg flex items-center gap-2 text-red-200">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmitting || rating === 0 || reviewText.trim().length < 10}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-4 rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>Processing...</>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Submit Review
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
