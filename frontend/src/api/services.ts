// 1. Import your teammate's new API layer functions directly
import type { RegisterRequest } from "../types";
import {
  login,
  signup,
  saveOnboardingPreferences,
} from "./restaurants";

const BASE_URL = "http://localhost:8000";

// Reusable core fetch wrapper (retained for custom native endpoints if needed)
async function handleRequest<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}


export const userService = {
  getOnlineLikedRestaurants: (userId: string | number) =>
    handleRequest<{
      user_id: string;
      online_liked_restaurants: {
        gmap_id: string;
        name: string;
        image_url: string;
      }[];
    }>(`/users/${userId}/restaurants/likes/online`),

  getOfflineLikedRestaurants: (userId: string | number) =>
    handleRequest<{
      user_id: string;
      offline_liked_restaurants: {
        gmap_id: string;
        name: string;
        image_url: string;
      }[];
    }>(`/users/${userId}/restaurants/likes/offline`),

  unlikeRestaurant: (userId: string, restaurantId: string) =>
    handleRequest(`/users/restaurants/${restaurantId}/like`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
      }),
    }),

  likeRestaurant: (userId: string, restaurantId: string) =>
    handleRequest(`/users/restaurants/${restaurantId}/like`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
      }),
    }),
};

export const vibeService = {
  submitMatch: async (userId: string, preferences: any) => {
    // Clean & simple: directly call the imported function!
    return await saveOnboardingPreferences(userId, preferences);
  },
};

export const authService = {
  // Bridges directly to teammate's login method using Axios under the hood
  login: async (username: string, password: string) => {
    return await login(username, password);
  },

  // Bridges directly to teammate's signup method
  register: async (data: RegisterRequest) => {
    // Note: Teammate's signup implementation currently expects only (username, password)
    return await signup(data);
  }
};