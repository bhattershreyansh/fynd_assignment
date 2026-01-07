const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ReviewSubmitRequest {
  name: string;
  rating: number;
  review_text: string;
}

export interface ReviewSubmitResponse {
  id: string;
  rating: number;
  review_text: string;
  user_response: string;
  created_at: string;
  status: string;
}

export interface AdminReviewItem {
  id: string;
  rating: number;
  review_text: string;
  summary: string | null;
  recommended_actions: string[] | null;
  user_response: string | null;
  created_at: string;
}

export interface AdminReviewsResponse {
  reviews: AdminReviewItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface AnalyticsResponse {
  total_reviews: number;
  average_rating: number;
  rating_distribution: Record<number, number>;
  recent_reviews_count: number;
}

export interface PriorityReviewsResponse {
  urgent_reviews: AdminReviewItem[];
  total_urgent: number;
  message: string;
}

export const api = {
  async submitReview(data: ReviewSubmitRequest): Promise<ReviewSubmitResponse> {
    const response = await fetch(`${API_BASE_URL}/api/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to submit review');
    }

    return response.json();
  },

  async getReviews(page = 1, pageSize = 50, rating?: number): Promise<AdminReviewsResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    if (rating) {
      params.append('rating', rating.toString());
    }

    const response = await fetch(`${API_BASE_URL}/api/reviews?${params}`);

    if (!response.ok) {
      throw new Error('Failed to fetch reviews');
    }

    return response.json();
  },

  async getAnalytics(): Promise<AnalyticsResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analytics`);

    if (!response.ok) {
      throw new Error('Failed to fetch analytics');
    }

    return response.json();
  },

  async getPriorityReviews(limit = 20): Promise<PriorityReviewsResponse> {
    const response = await fetch(`${API_BASE_URL}/api/reviews/priority?limit=${limit}`);

    if (!response.ok) {
      throw new Error('Failed to fetch priority reviews');
    }

    return response.json();
  },

  async exportReviews(rating?: number): Promise<Blob> {
    const params = rating ? `?rating=${rating}` : '';
    const response = await fetch(`${API_BASE_URL}/api/reviews/export${params}`);

    if (!response.ok) {
      throw new Error('Failed to export reviews');
    }

    return response.blob();
  },
};
