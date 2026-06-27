import { 
  login, 
  signup, 
  getUserRecommendations, 
  getSimilarRestaurants,
  saveOnboardingPreferences
} from './restaurants';

const BASE_URL = "http://localhost:8000/api";

// Reusable core fetch wrapper (retained for custom native endpoints if needed)
async function handleRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
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

// 2. Export specific, semantic API services mapped cleanly to your teammate's setup
export const restaurantService = {
  // Bridges to teammate's Collaborative Filtering endpoint
  getAll: async () => {
    // Uses a default placeholder user ID for now until state context management is added
    const data = await getUserRecommendations("default_user_id");
    // If their endpoint returns a structured object, adjust this mapping to extract the array
    return data.recommendations || data; 
  },
  
  // Bridges to teammate's Content-Based matching endpoint
  getSimilar: (restaurantName: string) => getSimilarRestaurants(restaurantName),
  
  getById: (id: string) => handleRequest<any>(`/restaurants/${id}`),
};

export const userService = {
  getProfile: () => handleRequest<{ name: string }>("/user/profile"),
  updateProfile: (data: any) => handleRequest("/user/profile", {
    method: "PUT",
    body: JSON.stringify(data),
  }),
};

export const vibeService = {
  submitMatch: async (preferences: any) => {
    // Dynamically grab the userId stored by your teammate's login block
    const userId = localStorage.getItem("userId") || "default_user_id"; 
    
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
  register: async (username: string, email: string, password: string) => {
    // Note: Teammate's signup implementation currently expects only (username, password)
    return await signup(username, password);
  }
};