export interface Restaurant {
  gmap_id: string;
  name: string;
  cuisine: string;
  avg_rating: number;
  price: '$' | '$$' | '$$$';
  image_url: string;
}


export interface Friend {
  user_id: string;
  name: string;
  username: string;
  avatar_index: number;
}


export type BudgetOption = "$" | "$$" | "$$$";
export type DistanceOption = "Walking Distance" | "Up to 15 Minutes" | "Up to 30 Minutes" | "Anywhere";
export type AccessibilityOption = "Required" | "Not Required";
export type DietaryOption = "None" | "Vegetarian" | "Vegan" | "Gluten Free";
export type DineOption = "Dine-in" | "Takeout" | "Both";

export type MatchingCategory =
  | "american"
  | "italian"
  | "chinese"
  | "mexican_latin"
  | "indian"
  | "cafe"
  | "breakfast_brunch"
  | "lunch"
  | "dinner"
  | "fast_food"
  | "vegetarian"
  | "halal";





export type UserData = {
  user_id: string;
  username: string;
  avatar_index: number;
  name: string;
};



export type RegisterRequest = {
  name: string;
  username: string;
  password: string;
  avatar_index: number;
  location: {
    type: "Point";
    coordinates: [number, number];
  };
};
