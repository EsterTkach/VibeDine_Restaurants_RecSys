import { useState } from "react";
import { useNavigate } from "react-router-dom";

import AppShell from "../layouts/AppShell";
import { demoUsers } from "../data/demoUsers";

import "./AuthPage.css";

export default function SignUpPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  const handleSignUp = () => {
    const exists = demoUsers.some(
      (user) =>
        user.username.toLowerCase() ===
        username.toLowerCase()
    );

    if (exists) {
      setError("This username is already taken.");
      return;
    }

    navigate("/loading");
  };

  return (
    <AppShell>
      <div className="auth-container">
        <div className="logo-section">

          <div className="floating-logo">
            🍽️
          </div>

          <h1 className="logo-text">
            VibeDine
          </h1>

          <p className="subtitle">
            Create your account
          </p>

        </div>

        <div className="auth-card">

          <input
            className="input"
            placeholder="Username"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          {error && (
            <span
              style={{
                color: "#D32F2F",
                fontSize: "14px",
              }}
            >
              {error}
            </span>
          )}

          <button
            className="primary-btn"
            onClick={handleSignUp}
          >
            Create Account →
          </button>

          <button
            className="secondary-btn"
            onClick={() => navigate("/login")}
          >
            Back To Login
          </button>

        </div>
      </div>
    </AppShell>
  );
}