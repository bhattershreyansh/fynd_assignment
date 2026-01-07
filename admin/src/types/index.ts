export interface Review {
  id: string;
  rating: number;
  review_text: string;
  summary: string | null;
  recommended_actions: string[] | null;
  user_response: string | null;
  created_at: string;
  updated_at: string;
}

export interface Analytics {
  total_reviews: number;
  average_rating: number;
  rating_distribution: Record<number, number>;
  recent_reviews_count: number;
}

export interface PriorityReviewsResponse {
  urgent_reviews: Review[];
  total_urgent: number;
  message: string;
}

export interface ReviewsResponse {
  reviews: Review[];
  total: number;
  page: number;
  page_size: number;
}
