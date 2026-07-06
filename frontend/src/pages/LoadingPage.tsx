import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import AppShell from "../layouts/AppShell";
import { getHomeCarousels, createGroupSession } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import { useHome } from "../contexts/HomeContext";
import { useLiked } from "../contexts/LikedContext";
import "./LoadingPage.css";

export default function LoadingPage() {
  const messages = [
    "Cooking your next obsession...",
    "Finding hidden gems...",
    "Matching your vibe...",
    "Searching for the perfect spot...",
    "Pairing food with your mood..."
  ];

  const [messageIndex, setMessageIndex] = useState(0);
  const navigate = useNavigate();
  const location = useLocation();
  const { userData } = useAuth();
  const { setCarousels, setLastLoad } = useHome();
  const { likedRestaurants } = useLiked();

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, 2200);

    const loadData = async () => {
      const nextPage = location.state?.nextPage || "/home";
      const userId = location.state?.user_id || userData.user_id;
      const mode = location.state?.mode;

      if (mode === "group") {
        const groupUserIds: string[] = location.state?.groupUserIds || [];
        const groupFilters: Record<string, unknown> =
          location.state?.groupFilters || {};

        try {
          const session = await createGroupSession(groupUserIds, groupFilters);
          navigate(nextPage, {
            replace: true,
            state: {
              ...location.state,
              groupSessionId: session.session_id,
              recommendation: session.recommendation,
            },
          });
        } catch (error: any) {
          const detail =
            error?.response?.data?.detail || error?.message || "Unknown error";
          console.error("Group session error:", detail, error?.response?.status);
          navigate("/group", {
            replace: true,
            state: {
              ...location.state,
              groupError: `Could not start a group session: ${detail}`,
            },
          });
        }
        return;
      }

      if (!userId) {
        navigate(nextPage, { replace: true, state: location.state });
        return;
      }

      try {
        const data = await getHomeCarousels(userId);
        setCarousels(data.carousels || []);
        setLastLoad({ userId, onlineLikesCount: likedRestaurants.length });
        navigate(nextPage, {
          replace: true,
          state: location.state,
        });
      } catch (error) {
        console.error("Failed to load home recommendations:", error);
        setCarousels([]);
        setLastLoad({ userId, onlineLikesCount: likedRestaurants.length });
        navigate(nextPage, {
          replace: true,
          state: location.state,
        });
      }
    };

    void loadData();

    return () => {
      clearInterval(interval);
    };
  }, [location.state, navigate, setCarousels, setLastLoad, userData.user_id, likedRestaurants.length, messages.length]);

  return (
    <AppShell>
      <div className="loading-container">

        <div className="loading-logo">
          🍽️
        </div>
        <h1 className="loading-title">
          VibeDine
        </h1>

        <p className="loading-message">
          {messages[messageIndex]}
        </p>

        <div className="loading-bar">
          <div className="loading-bar-fill" />
        </div>

        <div className="food-icons">
            🍣 🍕 🍔 🥗 🥐
        </div>

      </div>
    </AppShell>
  );
}