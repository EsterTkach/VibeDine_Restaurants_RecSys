import {
  createContext,
  useContext,
  useState,
  useCallback,
  useRef,
  type ReactNode,
} from "react";

import type { CarouselData } from "../types";

const LIKES_BEFORE_REFRESH = 3;

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
  const likeCountRef = useRef(0);

  const notifyLikeChanged = useCallback(() => {
    likeCountRef.current += 1;
    if (likeCountRef.current >= LIKES_BEFORE_REFRESH) {
      likeCountRef.current = 0;
      setHasLoadedHome(false);
    }
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