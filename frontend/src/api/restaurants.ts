import apiClient from './client';
import type { ApiRecommendationResponse } from '../types';

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

export async function signup(username: string, password: string): Promise<{ message: string; user_id: string }> {
  const response = await apiClient.post('/users/signup', { username, password });
  return response.data;
}

export async function saveOnboardingPreferences(
  userId: string,
  preferences: {
    favorite_categories: string[];
    favorite_atmospheres: string[];
    accessibility: string;
    dietary_restrictions: string;
  }
) {
  const response = await apiClient.post(
    `/users/${userId}/onboarding-preferences`,
    {
      preferences,
    }
  );

  return response.data;
}

export async function login(username: string, password: string): Promise<{ message: string; user_id: string; username: string }> {
  const response = await apiClient.post('/users/login', { username, password });
  return response.data;
}

export async function getHomeCarousels(userId: string, topK = 25) {
  const response = await apiClient.get("/recommend/home-carousels", {
    params: {
      user_id: userId,
      top_k: topK,
    },
  });
  
  return response.data;
}

export async function getVibeMatchRecommendations(
  userId: string,
  filters: any
) {
  const response = await apiClient.post(
    `/recommend/vibe-match/${userId}`,
    filters
  );
  
  return response.data;
}

export type GroupRecommendation = {
  gmap_id: string;
  name: string;
  avg_hybrid_score?: number;
  users_supported?: number;
  coverage?: number;
  group_score?: number;
};

export type GroupSessionResponse = {
  session_id: string;
  recommendation: GroupRecommendation | null;
};

export async function createGroupSession(userIds: string[]) {
  const response = await apiClient.post<GroupSessionResponse>("/groups/session", {
    user_ids: userIds,
    top_k: 1,
    per_user_k: 50,
  });

  return response.data;
}

export async function submitGroupSessionFeedback(
  sessionId: string,
  currentRestaurant: string,
  affectedUserIds: string[],
  reason: string,
) {
  const response = await apiClient.post<GroupSessionResponse>(
    `/groups/session/${sessionId}/feedback`,
    {
      current_restaurant: currentRestaurant,
      affected_user_ids: affectedUserIds,
      reason,
      top_k: 1,
      per_user_k: 50,
    },
  );

  return response.data;
}


export type GroupRecommendation = {
  gmap_id: string;
  name: string;
  avg_hybrid_score?: number;
  users_supported?: number;
  coverage?: number;
  group_score?: number;
};

export type GroupSessionResponse = {
  session_id: string;
  recommendation: GroupRecommendation | null;
};

export async function createGroupSession(userIds: string[]) {
  const response = await apiClient.post<GroupSessionResponse>("/groups/session", {
    user_ids: userIds,
    top_k: 1,
    per_user_k: 50,
  });

  return response.data;
}

export async function submitGroupSessionFeedback(
  sessionId: string,
  currentRestaurant: string,
  affectedUserIds: string[],
  reason: string,
) {
  const response = await apiClient.post<GroupSessionResponse>(
    `/groups/session/${sessionId}/feedback`,
    {
      current_restaurant: currentRestaurant,
      affected_user_ids: affectedUserIds,
      reason,
      top_k: 1,
      per_user_k: 50,
    },
  );

  return response.data;
}
