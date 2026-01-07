// API Request/Response Types

export interface ReviewSubmitRequest {
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

export interface Analytics {
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
