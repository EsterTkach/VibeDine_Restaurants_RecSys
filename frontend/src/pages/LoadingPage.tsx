import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import AppShell from "../layouts/AppShell";
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

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, 2200);
    
    const timeout = setTimeout(() => {

      const nextPage =
        location.state?.nextPage || "/home";

      navigate(
        nextPage,
        {
          state: location.state,
        }
      );

    }, 2200);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
    }, [navigate, location]);
    

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