import apiClient from './client';
import type { ApiRecommendationResponse } from '../types';

// Set to true to use mock data, false to call the real backend
export const USE_MOCK = true;

export async function getUserRecommendations(userId: string, topK = 10): Promise<ApiRecommendationResponse> {
  const response = await apiClient.get<ApiRecommendationResponse>(`/recommend/cf/${userId}`, {
    params: { top_k: topK },
  });
  return response.data;
}

export async function getSimilarRestaurants(restaurantName: string, topK = 10): Promise<ApiRecommendationResponse> {
  const response = await apiClient.get<ApiRecommendationResponse>(`/recommend/cb/${encodeURIComponent(restaurantName)}`, {
    params: { top_k: topK },
  });
  return response.data;
}

export async function signup(username: string): Promise<{ message: string; user_id: string }> {
  const response = await apiClient.post('/users/signup', { username });
  return response.data;
}
