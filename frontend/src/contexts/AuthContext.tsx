import { createContext, useContext, useState } from "react";

type AuthContextType = {
  userId: string;
  username: string;
  setUserId: (userId: string) => void;
  setUsername: (username: string) => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userId, setUserId] = useState(
    localStorage.getItem("user_id") || "");
  const [username, setUsername] = useState(
    localStorage.getItem("username") || "");

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