import "./AuthPage.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { authService } from "../api/services";
import { useAuth } from "../contexts/AuthContext";

export default function SignUpPage() {
  const navigate = useNavigate();

  const { userData, setUserData } = useAuth();

  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSignUp = async () => {
    if (!userData.username.trim() || !password.trim()) {
      setError("Please fill in all fields");
      return;
    }

    try {
      setError("");
      setLoading(true);

      const response = await authService.register(userData.username, password); // Email is empty string for now
      setUserData(response.user_data);

      localStorage.setItem("user_data", JSON.stringify(response.user_data));

      navigate("/onboarding", {
        replace: true,
        state: {
          userData: response.user_data,
        },
      });
    } catch (apiError) {
      console.warn("Backend sign up failed.", apiError);
      const status = (apiError as any)?.response?.status;
      if (status === 409) {
        setError("Username already exists. Please choose another one.");
      } else {
        setError("Sign up failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="auth-container">
        <div className="logo-section">
          <div className="floating-logo">🍽️</div>
          <h1 className="logo-text">VibeDine</h1>
          <p className="subtitle">Create your account</p>
        </div>

        <div className="auth-card">
          <input
            className="input"
            placeholder="Username"
            value={userData.username}
            disabled={loading}
            onChange={(e) =>
              setUserData({
                ...userData,
                username: e.target.value,
              })
            }
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            value={password}
            disabled={loading}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <span style={{ color: "#D32F2F", fontSize: "14px", marginTop: "-4px", marginBottom: "4px" }}>
              {error}
            </span>
          )}

          <button
            className="primary-btn"
            onClick={handleSignUp}
            disabled={loading}
          >
            {loading ? "Creating..." : "Create Account →"}
          </button>

          <button
            className="secondary-btn"
            onClick={() => navigate("/login")}
            disabled={loading}
          >
            Back To Login
          </button>
        </div>
      </div>
    </AppShell>
  );
}
