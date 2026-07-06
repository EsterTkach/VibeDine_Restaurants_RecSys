import {
  createContext,
  useContext,
  useState,
  useCallback,
  useRef,
  useEffect,
  type ReactNode,
} from "react";

import type { CarouselData } from "../types";

// Small delay before flushing an invalidation so rapid successive likes
// coalesce into a single home refresh instead of hammering the backend.
const LIKE_INVALIDATION_DEBOUNCE_MS = 800;

type HomeContextType = {
  carousels: CarouselData[];
  setCarousels: React.Dispatch<React.SetStateAction<CarouselData[]>>;
  hasLoadedHome: boolean;
  setHasLoadedHome: React.Dispatch<React.SetStateAction<boolean>>;
  notifyLikeChanged: () => void;
};

const HomeContext = createContext<HomeContextType | null>(null);

export function HomeProvider({ children }: { children: ReactNode }) {
  const [carousels, setCarousels] = useState<CarouselData[]>([]);
  const [hasLoadedHome, setHasLoadedHome] = useState(false);
  const invalidationTimeoutRef = useRef<number | null>(null);

  // Every like or unlike (from anywhere) marks the home feed stale. We
  // DON’T clear `carousels` here — the user stays on their current view with
  // no jarring loader. The next time HomePage mounts (i.e., navigation back
  // to Home from another route), its effect sees `hasLoadedHome === false`
  // and refetches, showing the loader then. A short debounce coalesces bursts.
  const notifyLikeChanged = useCallback(() => {
    if (invalidationTimeoutRef.current !== null) {
      window.clearTimeout(invalidationTimeoutRef.current);
    }
    invalidationTimeoutRef.current = window.setTimeout(() => {
      invalidationTimeoutRef.current = null;
      setHasLoadedHome(false);
    }, LIKE_INVALIDATION_DEBOUNCE_MS);
  }, []);

  useEffect(() => {
    return () => {
      if (invalidationTimeoutRef.current !== null) {
        window.clearTimeout(invalidationTimeoutRef.current);
      }
    };
  }, []);

  return (
    <HomeContext.Provider
      value={{
        carousels,
        setCarousels,
        hasLoadedHome,
        setHasLoadedHome,
        notifyLikeChanged,
      }}
    >
      {children}
    </HomeContext.Provider>
  );
}

export function useHome() {
  const context = useContext(HomeContext);

  if (!context) {
    throw new Error("useHome must be used inside HomeProvider");
  }

  return context;
}