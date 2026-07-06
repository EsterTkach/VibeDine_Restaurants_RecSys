import { createContext, useContext, useState, useEffect, useRef } from "react";

import { userService } from "../api/services";
import { useAuth } from "./AuthContext";

export type Restaurant = {
  gmap_id: string;
  name: string;
  image_url: string;
};

// A user needs this many total likes (offline history + in-app likes) before
// their taste starts influencing recommendations. Mirrored in the backend at
// `api/routes/recommendations.py` (`is_cold_start = augmented_likes < 3`).
export const PERSONALIZATION_THRESHOLD = 3;

export type PersonalizationToast = {
  id: number;
  message: string;
  variant: "progress" | "unlock";
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

  augmentedLikesCount: number;
  isPersonalized: boolean;
  personalizationToast: PersonalizationToast | null;
  dismissPersonalizationToast: () => void;
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

  // Personalization progress: transient toast + count of both offline & online
  // likes. `hydratedForUserRef` tracks whether the initial fetches for the
  // current user have completed — we only start listening for real like
  // events after that so we don’t misfire on sign-in / user switch.
  const [personalizationToast, setPersonalizationToast] =
    useState<PersonalizationToast | null>(null);
  const previousCountRef = useRef<number | null>(null);
  const hydratedForUserRef = useRef<string | null>(null);
  const augmentedLikesCount =
    likedRestaurants.length + offlineLikedRestaurants.length;
  const isPersonalized = augmentedLikesCount >= PERSONALIZATION_THRESHOLD;

  const dismissPersonalizationToast = () => setPersonalizationToast(null);

  // Reset hydration + count tracking whenever the logged-in user changes,
  // so a switched-account sign-in doesn’t fire the toast for pre-existing likes.
  useEffect(() => {
    hydratedForUserRef.current = null;
    previousCountRef.current = null;
    setPersonalizationToast(null);
  }, [userData.user_id]);

  // Once BOTH online + offline fetches have completed for the current user,
  // mark this user as “hydrated” and seed the previous count baseline.
  useEffect(() => {
    if (!userData.user_id) return;
    if (hydratedForUserRef.current === userData.user_id) return;
    if (!hasLoadedLikedRestaurants || !hasLoadedOfflineLikedRestaurants) return;

    hydratedForUserRef.current = userData.user_id;
    previousCountRef.current = augmentedLikesCount;
  }, [
    userData.user_id,
    hasLoadedLikedRestaurants,
    hasLoadedOfflineLikedRestaurants,
    augmentedLikesCount,
  ]);

  useEffect(() => {
    // Only react to changes AFTER the current user’s initial data has landed.
    if (hydratedForUserRef.current !== userData.user_id) return;

    const previous = previousCountRef.current;
    previousCountRef.current = augmentedLikesCount;

    if (previous === null) return;
    // Only fire on a real single-like increment. Skips bulk jumps from
    // fetches finishing (online+offline landing in the same commit can push
    // the count by >1) and any decreases (unlikes).
    if (augmentedLikesCount !== previous + 1) return;

    if (
      augmentedLikesCount >= PERSONALIZATION_THRESHOLD &&
      previous < PERSONALIZATION_THRESHOLD
    ) {
      setPersonalizationToast({
        id: Date.now(),
        variant: "unlock",
        message: "✨ We’re now learning what you love!",
      });
      return;
    }

    if (augmentedLikesCount < PERSONALIZATION_THRESHOLD) {
      const remaining = PERSONALIZATION_THRESHOLD - augmentedLikesCount;
      setPersonalizationToast({
        id: Date.now(),
        variant: "progress",
        message: `❤️ ${remaining} more like${remaining === 1 ? "" : "s"} to unlock personalized picks`,
      });
    }
  }, [augmentedLikesCount, userData.user_id]);

  useEffect(() => {
    if (!personalizationToast) return;
    const timeoutId = window.setTimeout(() => {
      setPersonalizationToast((current) =>
        current && current.id === personalizationToast.id ? null : current,
      );
    }, 3200);
    return () => window.clearTimeout(timeoutId);
  }, [personalizationToast]);

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
    } catch (error) {
      console.error("Failed to fetch online liked restaurants", error);
    } finally {
      // Always mark as loaded so the personalization hydration guard completes,
      // even when the user has no likes yet or the endpoint errors out.
      setHasLoadedLikedRestaurants(true);
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
    } catch (error) {
      console.error("Failed to fetch offline liked restaurants", error);
    } finally {
      // Always mark as loaded so the personalization hydration guard completes,
      // even for brand-new users who aren’t in the offline CF matrix.
      setHasLoadedOfflineLikedRestaurants(true);
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
        augmentedLikesCount,
        isPersonalized,
        personalizationToast,
        dismissPersonalizationToast,
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
