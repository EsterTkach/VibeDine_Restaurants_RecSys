import { useEffect, useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { FaApple, FaXTwitter } from "react-icons/fa6";
import AppShell from "../layouts/AppShell";
import { useNavigate } from "react-router-dom";
import { authService } from "../api/services";
import { useAuth } from "../contexts/AuthContext";
import { preloadHomeData } from "../api/home";

export default function AuthPage() {
  const navigate = useNavigate();
  
  const {username, setUsername, setUserId} = useAuth();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);

  useEffect(() => {
    setUsername("");
    setError("");
    setPassword("");
  }, [setUsername]);

  const showComingSoon = () => {
    setShowToast(true);
    setTimeout(() => {
      setShowToast(false);
    }, 2500);
  };

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setError("Please fill in all fields");
      return;
    }

    try {
      setError("");
      setLoading(true);

      console.log("Trying login:", username, password);
      // 1. Try hitting the live backend service first
      const data = await authService.login(username, password);
      console.log("Login response:", username,password);
      setUserId(data.user_id);
      setUsername(data.username);
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("username", data.username);
      //preloadHomeData(data.user_id);
      // If server returns a token/user, pass user data directly to the loading view
      navigate("/loading", { state: { username: data.username } });

    } catch (apiError) {
      const status = (apiError as any)?.response?.status;
      if (status === 401) {
        setError("Invalid username or password, please try again");
      } else {
        setError("Login failed. Please try again.");
      }
      console.log(apiError);
      console.warn("Backend login failed or offline.", apiError);
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
          <p className="subtitle">
            Personalized dining recommendations based on your taste, vibe and friends!
          </p>
        </div>

        <div className="auth-card">
          <input
            className="input"
            placeholder="Username"
            value={username}
            disabled={loading}
            onChange={(e) => setUsername(e.target.value)}
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
            onClick={handleLogin}
            disabled={loading}
          >
            {loading ? "Signing In..." : "Sign In →"}
          </button>

          <button 
            className="secondary-btn" 
            onClick={() => navigate("/signup")}
            disabled={loading}
          >
            Create Account
          </button>

          <div className="divider">or continue with</div>

          <button className="social-btn" onClick={showComingSoon} disabled={loading}>
            <FcGoogle size={20} />
            Continue with Google
          </button>

          <button className="social-btn" onClick={showComingSoon} disabled={loading}>
            <FaApple size={20} />
            Continue with Apple
          </button> 

          <button className="social-btn" onClick={showComingSoon} disabled={loading}>
            <FaXTwitter size={18} />
            Continue with X
          </button>
        </div>
      </div>

      {showToast && (
        <div className="toast">
          🚀 Social login is coming soon
        </div>
      )}
    </AppShell>
  );
}