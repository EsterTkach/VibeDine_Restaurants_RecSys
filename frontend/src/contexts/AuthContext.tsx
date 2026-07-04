import { createContext, useContext, useState } from "react";

type AuthContextType = {
  userId: string;
  username: string;
  setUserId: (userId: string) => void;
  setUsername: (username: string) => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

const getStoredUserId = () => localStorage.getItem("user_id") || localStorage.getItem("userId") || "";
const getStoredUsername = () => localStorage.getItem("username") || "";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userId, setUserIdState] = useState(getStoredUserId);
  const [username, setUsernameState] = useState(getStoredUsername);

  const setUserId = (nextUserId: string) => {
    setUserIdState(nextUserId);
    if (nextUserId) {
      localStorage.setItem("user_id", nextUserId);
      localStorage.setItem("userId", nextUserId);
    } else {
      localStorage.removeItem("user_id");
      localStorage.removeItem("userId");
    }
  };

  const setUsername = (nextUsername: string) => {
    setUsernameState(nextUsername);
    if (nextUsername) {
      localStorage.setItem("username", nextUsername);
    } else {
      localStorage.removeItem("username");
    }
  };

  return (
    <AuthContext.Provider
      value={{
        userId,
        setUserId,
        username,
        setUsername,
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