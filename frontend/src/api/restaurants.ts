import apiClient from './client';
import type {Friend, RegisterRequest, UserData } from '../types';


export async function signup(data: RegisterRequest,): Promise<{ message: string; user_data: UserData }> {
  const response = await apiClient.post('/users/signup', data);
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
    { preferences }
  );
  return response.data;
}

export async function login(username: string, password: string): Promise<{ message: string; user_data: UserData }> {
  const response = await apiClient.post("/users/login", { username, password });
  return response.data;
}

// Friends
export async function getFriends(userId: string): Promise<Friend[]> {
  const response = await apiClient.get<Friend[]>(`/users/${userId}/friends`);
  return response.data;
}

export async function searchUsers(query: string, currentUserId: string): Promise<Friend[]> {
  const response = await apiClient.get<Friend[]>('/users/search', {
    params: { username: query, user_id: currentUserId },
  });
  return response.data;
}

export async function addFriend(userId: string, friendId: string): Promise<void> {
  await apiClient.post(`/users/${userId}/friends`, { friend_id: friendId });
}

export async function removeFriend(userId: string, friendId: string): Promise<void> {
  await apiClient.delete(`/users/${userId}/friends/${friendId}`);
}

// Home carousels
export async function getHomeCarousels(userId: string, topK = 25) {
  const response = await apiClient.get("/recommend/home-carousels", {
    params: { user_id: userId, top_k: topK },
    timeout: 60000,
  });
  return response.data;
}

export async function getVibeMatchRecommendations(userId: string, filters: any) {
  const response = await apiClient.post(`/recommend/vibe-match/${userId}`, filters, {
    timeout: 60000,
  });
  return response.data;
}

// Group sessions
export type GroupRecommendation = {
  gmap_id: string;
  name: string;
  avg_rating?: number;
  price?: string;
  image_url?: string;
  cuisines?: string[];
  avg_hybrid_score?: number;
  users_supported?: number;
  coverage?: number;
  group_score?: number;
};

export type GroupSessionResponse = {
  session_id: string;
  recommendation: GroupRecommendation | null;
};

export async function createGroupSession(userIds: string[], filters?: Record<string, unknown>) {
  const response = await apiClient.post<GroupSessionResponse>(
    "/groups/session",
    {
      user_ids: userIds,
      top_k: 1,
      per_user_k: 50,
      filters: filters ?? {},
    },
    { timeout: 60000 },
  );
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
    { timeout: 60000 },
  );
  return response.data;
}
