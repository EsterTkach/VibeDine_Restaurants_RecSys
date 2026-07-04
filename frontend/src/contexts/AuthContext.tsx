import { createContext, useContext, useState } from "react";

import type { UserData } from "../types";

type AuthContextType = {
  userData: UserData;
  setUserData: React.Dispatch<React.SetStateAction<UserData>>;
};

const defaultUserData: UserData = {
  user_id: "",
  username: "",
  avatar_index: 0,
  name: "",
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userData, setUserData] = useState<UserData>(() => {
    const stored = localStorage.getItem("user_data");

    if (!stored) return defaultUserData;

    try {
      return JSON.parse(stored) as UserData;
    } catch {
      return defaultUserData;
    }
  });

  return (
    <AuthContext.Provider
      value={{
        userData,
        setUserData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}