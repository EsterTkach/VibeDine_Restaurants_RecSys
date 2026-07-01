import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

import type { CarouselData } from "../types";

type HomeContextType = {
  carousels: CarouselData[];
  setCarousels: React.Dispatch<React.SetStateAction<CarouselData[]>>;
  hasLoadedHome: boolean;
  setHasLoadedHome: React.Dispatch<React.SetStateAction<boolean>>;
};

const HomeContext = createContext<HomeContextType | null>(null);

export function HomeProvider({ children }: { children: ReactNode }) {
  const [carousels, setCarousels] = useState<CarouselData[]>([]);
  const [hasLoadedHome, setHasLoadedHome] = useState(false);

  return (
    <HomeContext.Provider
      value={{
        carousels,
        setCarousels,
        hasLoadedHome,
        setHasLoadedHome,
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