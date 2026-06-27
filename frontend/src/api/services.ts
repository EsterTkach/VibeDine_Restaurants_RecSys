const BASE_URL = "http://localhost:8000/api";

// Reusable core fetch wrapper to avoid repeating try/catch headers setup
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

// Export specific, semantic API services for your components
export const restaurantService = {
  getAll: () => handleRequest<any[]>("/restaurants"),
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
  submitMatch: (vibeData: any) => handleRequest("/vibe-match", {
    method: "POST",
    body: JSON.stringify(vibeData),
  }),
};

export const authService = {
  // Sign In call endpoint blueprint
  login: async (username: string, password: string) => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error(`Login failed with status: ${response.status}`);
    }

    return response.json(); 
  },

  // Sign Up call endpoint blueprint
  register: async (username: string, email: string, password: string) => {
    const response = await fetch(`${BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
    });

    if (!response.ok) {
      throw new Error(`Registration failed with status: ${response.status}`);
    }

    return response.json();
  }
};