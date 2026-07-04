export interface Restaurant {
  gmap_id: string;
  name: string;
  cuisine: string;
  avg_rating: number;
  price: '$' | '$$' | '$$$';
  image_url: string;
}

export interface RowConfig {
  id: string;
  title: string;
  emoji: string;
  restaurants: Restaurant[];
}

export interface CarouselData {
  id: string;
  title: string;
  items: Restaurant[];
}

export interface User {
  user_id: string;
  name: string;
  username: string;
  password: string;
  avatar_url: string;
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

export type PreferenceOption = 
  | "budget" 
  | "accessibility" 
  | "dietary" 
  | "distance" 
  | "dineOption";

export type BudgetOption = "$" | "$$" | "$$$";
export type DistanceOption = "Walking Distance" | "Up to 15 Minutes" | "Up to 30 Minutes" | "Anywhere";
export type AccessibilityOption = "Required" | "Not Required";
export type DietaryOption = "None" | "Vegetarian" | "Vegan" | "Gluten Free";
export type DineOption = "Dine-in" | "Takeout" | "Both";

export type MatchingCategory = 
  | "italian" 
  | "japanese" 
  | "mexican" 
  | "thai" 
  | "indian" 
  | "french" 
  | "korean" 
  | "datenight" 
  | "groups" 
  | "coffee" 
  | "lunch" 
  | "dessert";

export interface VibeMatcherState {
  selectedPreferences: PreferenceOption[];
  selectedCategories: MatchingCategory[];
  preferences: {
    budget?: BudgetOption;
    distance?: DistanceOption;
    accessibility?: AccessibilityOption;
    dietary?: DietaryOption;
    dineOption?: DineOption;
  };
}
