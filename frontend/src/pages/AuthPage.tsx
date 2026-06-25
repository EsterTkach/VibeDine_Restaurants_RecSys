import { useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { FaApple, FaXTwitter } from "react-icons/fa6";
import AppShell from "../layouts/AppShell";
import "./AuthPage.css";
import { useNavigate } from "react-router-dom";
import { demoUsers } from "../data/demoUsers";

export default function AuthPage() {

  const [showToast, setShowToast] = useState(false);

  // const messages = [
  //   "Cooking your next obsession...",
  //   "Finding hidden gems...",
  //   "Matching your vibe...",
  //   "Searching for the perfect spot...",
  //   "Pairing food with your mood..."
  // ];

  // const [messageIndex, setMessageIndex] = useState(0);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setMessageIndex(prev => (prev + 1) % messages.length);
  //   }, 2200);

  //   return () => clearInterval(interval);
  // }, []);

  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  const showComingSoon = () => {
    setShowToast(true);

    setTimeout(() => {
      setShowToast(false);
    }, 2500);
  };
  const handleLogin = () => {
  const validUser = demoUsers.find(
    (user) =>
      user.username === username &&
      user.password === password
  );

  if (!validUser) {
    setError(
      "Invalid username or password"
    );
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
            Personalized dining recommendations
            based on your taste, vibe and friends!
          </p>

          {/* <div className="rotating-message">
            {messages[messageIndex]}
          </div> */}

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

          <button className="primary-btn" onClick={handleLogin}>
            Sign In →
          </button>

          <button className="secondary-btn" onClick={() => navigate("/signup")}>
            Create Account
          </button>

          <div className="divider">
            or continue with
          </div>

          <button
            className="social-btn"
            onClick={showComingSoon}
          >
            <FcGoogle size={20} />
            Continue with Google
          </button>

          <button
            className="social-btn"
            onClick={showComingSoon}
          >
            <FaApple size={20} />
            Continue with Apple
          </button>   

          <button
            className="social-btn"
            onClick={showComingSoon}
          >
            <FaXTwitter size={18} />
            Continue with X
          </button>

        </div>

      </div>
      {
      showToast && (
        <div className="toast">
          🚀 Social login is coming soon
        </div>
      )
    }
    </AppShell>
  );
}