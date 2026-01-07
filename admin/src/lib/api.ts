import type {
    AdminReviewsResponse,
    Analytics,
    PriorityReviewsResponse,
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = {
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

    async getAnalytics(): Promise<Analytics> {
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
