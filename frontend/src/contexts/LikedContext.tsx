import { createContext, useContext, useState, useEffect } from "react";

import { userService } from "../api/services";
import { useAuth } from "./AuthContext";

export type Restaurant = {
  gmap_id: string;
  name: string;
  image_url: string;
};

type LikedContextType = {
  likedRestaurants: Restaurant[];
  offlineLikedRestaurants: Restaurant[];
  loading: boolean;

  fetchLikedRestaurants: () => Promise<void>;
  fetchOfflineLikedRestaurants: (force?: boolean) => Promise<void>;

  likeRestaurant: (restaurantId: string) => Promise<void>;
  unlikeRestaurant: (restaurantId: string) => Promise<void>;

  setLikedRestaurants: React.Dispatch<React.SetStateAction<Restaurant[]>>;
};

const LikedContext = createContext<LikedContextType | null>(null);

export function LikedProvider({ children }: { children: React.ReactNode }) {
  const { userData } = useAuth();

  // User's favorite restaurants.
  const [likedRestaurants, setLikedRestaurants] = useState<Restaurant[]>([]);

  // Loading state for the initial favorites fetch.
  const [loading, setLoading] = useState(false);

  // Ensures favorites are fetched only once per logged-in user.
  const [hasLoadedLikedRestaurants, setHasLoadedLikedRestaurants] =
    useState(false);

  // Restaurants the user liked in the past (offline history).
  const [offlineLikedRestaurants, setOfflineLikedRestaurants] = useState<
    Restaurant[]
  >([]);

  // Ensures offline favorites are fetched only once per logged-in user.
  const [
    hasLoadedOfflineLikedRestaurants,
    setHasLoadedOfflineLikedRestaurants,
  ] = useState(false);

  useEffect(() => {
    if (!userData.user_id) return;

    setLikedRestaurants([]);
    setOfflineLikedRestaurants([]);

    setHasLoadedLikedRestaurants(false);
    setHasLoadedOfflineLikedRestaurants(false);

    fetchLikedRestaurants(true);
    fetchOfflineLikedRestaurants(true);
  }, [userData.user_id]);

  async function fetchLikedRestaurants(force = false) {
    // When force is true, bypass the cache and always fetch fresh data.

    if (!userData.user_id) {
      console.warn("No user ID found. Cannot fetch liked restaurants.");
      return;
    }
    if (!force && hasLoadedLikedRestaurants) return;

    try {
      setLoading(true);

      const data = await userService.getOnlineLikedRestaurants(userData.user_id);

      setLikedRestaurants(data.online_liked_restaurants);
      setHasLoadedLikedRestaurants(true);
    } finally {
      setLoading(false);
    }
  }

  async function unlikeRestaurant(restaurantId: string) {
    await userService.unlikeRestaurant(userData.user_id, restaurantId);

    setLikedRestaurants((prev) =>
      prev.filter((r) => r.gmap_id !== restaurantId),
    );
  }

  async function likeRestaurant(restaurantId: string) {
    await userService.likeRestaurant(userData.user_id, restaurantId);

    await fetchLikedRestaurants(true);
  }

  async function fetchOfflineLikedRestaurants(force = false) {
    // When force is true, bypass the cache and always fetch fresh data.

    if (!userData.user_id) {
      console.warn("No user ID found. Cannot fetch offline liked restaurants.");
      return;
    }

    if (!force && hasLoadedOfflineLikedRestaurants) return;

    try {
      const data = await userService.getOfflineLikedRestaurants(
        userData.user_id,
      );

      setOfflineLikedRestaurants(data.offline_liked_restaurants);
      setHasLoadedOfflineLikedRestaurants(true);
    } catch (error) {
      console.error("Failed to fetch offline liked restaurants", error);
    }
  }

  return (
    <LikedContext.Provider
      value={{
        likedRestaurants,
        offlineLikedRestaurants,
        loading,
        fetchLikedRestaurants,
        fetchOfflineLikedRestaurants,
        likeRestaurant,
        unlikeRestaurant,
        setLikedRestaurants,
      }}
    >
      {children}
    </LikedContext.Provider>
  );
}

export function useLiked() {
  const context = useContext(LikedContext);

  if (!context) {
    throw new Error("useLiked must be used inside LikedProvider");
  }

  return context;
}
