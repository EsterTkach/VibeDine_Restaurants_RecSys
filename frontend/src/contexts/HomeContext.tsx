import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";

import type { CarouselData } from "../types";

// Snapshot of the state at the last successful home fetch. HomePage compares
// (userId, onlineLikesCount) on mount and only refetches when either changed.
export type HomeLoadSnapshot = {
  userId: string;
  onlineLikesCount: number;
};

type HomeContextType = {
  carousels: CarouselData[];
  setCarousels: React.Dispatch<React.SetStateAction<CarouselData[]>>;
  lastLoad: HomeLoadSnapshot | null;
  setLastLoad: (snapshot: HomeLoadSnapshot | null) => void;
};

const HomeContext = createContext<HomeContextType | null>(null);

export function HomeProvider({ children }: { children: ReactNode }) {
  const [carousels, setCarousels] = useState<CarouselData[]>([]);
  const [lastLoad, setLastLoadState] =
    useState<HomeLoadSnapshot | null>(null);

  const setLastLoad = useCallback(
    (snapshot: HomeLoadSnapshot | null) => setLastLoadState(snapshot),
    [],
  );

  return (
    <HomeContext.Provider
      value={{
        carousels,
        setCarousels,
        lastLoad,
        setLastLoad,
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