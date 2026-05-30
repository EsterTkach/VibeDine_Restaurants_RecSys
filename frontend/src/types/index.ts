export interface Restaurant {
  gmap_id: string;
  name: string;
  category: string;
  avg_rating: number;
  review_count: number;
  image_url: string;
  price_level?: '$' | '$$' | '$$$' | '$$$$';
  service_options?: string[];
  dining_options?: string[];
  address?: string;
  is_open?: boolean;
}

export interface RowConfig {
  id: string;
  title: string;
  emoji: string;
  restaurants: Restaurant[];
}

export interface User {
  user_id: string;
  username: string;
  email?: string;
  avatar_url?: string;
  member_since?: string;
  review_count: number;
  liked_restaurants: Restaurant[];
}

export interface ApiRecommendation {
  gmap_id: string;
  name: string;
  avg_rating?: number;
  review_count?: number;
  similarity_score?: number;
  predicted_rating?: number;
}

export interface ApiRecommendationResponse {
  recommendation_type?: string;
  recommendations: ApiRecommendation[];
}
