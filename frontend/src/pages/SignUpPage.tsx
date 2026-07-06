import "./AuthPage.css";
import "./SignUpPage.css";
import { useState } from "react";
import { Search } from "lucide-react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { authService } from "../api/services";
import FoodAvatar from "../components/FoodAvatar";
import { useAuth } from "../contexts/AuthContext";

export default function SignUpPage() {
  const navigate = useNavigate();

  const { setUserData } = useAuth();

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [avatarIndex, setAvatarIndex] = useState(0);
  const [location, setLocation] = useState<{
    type: "Point";
    coordinates: [number, number];
  } | null>(null);

  const [locationQuery, setLocationQuery] = useState("");
  const [locationName, setLocationName] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const isInCalifornia = (longitude: number, latitude: number) => {
    return (
      latitude >= 32.5 &&
      latitude <= 42.1 &&
      longitude >= -124.5 &&
      longitude <= -114.1
    );
  };

  const handleSearchLocation = async () => {
    if (!locationQuery.trim()) {
      setError("Please enter a location to search");
      return;
    }

    try {
      setError("");

      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${encodeURIComponent(
          locationQuery,
        )}&limit=1`,
      );

      const data = await response.json();

      if (!data.length) {
        setError("Location not found. Please try another search.");
        return;
      }

      const result = data[0];

      if (result.address?.state !== "California") {
        setLocation(null);
        setLocationName("");
        setError("VibeDine currently supports restaurants in California only. Please choose a location in California.");
        return;
      }

      const longitude = Number(result.lon);
      const latitude = Number(result.lat);

      setLocation({
        type: "Point",
        coordinates: [longitude, latitude],
      });

      setLocationName(result.display_name);
    } catch (error) {
      console.error(error);
      setError("Failed to search location. Please try again.");
    }
  };

  const handleGetLocation = () => {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        setError("");

        const location = {
          type: "Point" as const,
          coordinates: [
            position.coords.longitude,
            position.coords.latitude,
          ] as [number, number],
        };

        if (
          !isInCalifornia(position.coords.longitude, position.coords.latitude)
        ) {
          setLocation(null);
          setLocationName("");
          setError("Please choose a location in California.");
          return;
        }

        setLocation(location);

        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.coords.latitude}&lon=${position.coords.longitude}`,
          );

          const data = await response.json();

          setLocationName(data.display_name);
        } catch (error) {
          console.error("Failed to resolve location name", error);
        }
      },
      () => {
        setError("Could not get your location. Please allow location access.");
      },
    );
  };

  const handleSignUp = async () => {
    if (!name.trim() || !username.trim() || !password.trim() || !location) {
      setError("Please fill in all fields");
      return;
    }

    try {
      setError("");
      setLoading(true);

      const response = await authService.register({
        name,
        username,
        password,
        avatar_index: avatarIndex,
        location,
      });

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
          <h2 className="logo-text">VibeDine</h2>
          <p className="subtitle">Create your account</p>
        </div>

        <div className="auth-card">
          <input
            className="input"
            placeholder="Name"
            value={name}
            disabled={loading}
            onChange={(e) => {
              const value = e.target.value.replace(/[^a-zA-Zא-ת\s'-]/g, "");
              setName(value);
            }}
          />

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

          <div className="location-search-wrapper">
            <input
              className="input location-search-input"
              placeholder="Location"
              value={locationQuery}
              disabled={loading}
              onChange={(e) => setLocationQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSearchLocation();
                }
              }}
            />

            <div className="location-actions">
              <button
                type="button"
                className="location-search-btn"
                onClick={handleSearchLocation}
                disabled={loading}
              >
                <Search size={20} />
              </button>

              <button
                type="button"
                className="location-search-btn"
                onClick={handleGetLocation}
                disabled={loading}
                title="Use my current location"
              >
                📍
              </button>
            </div>
          </div>

          {locationName && (
            <div className="location-preview">📍 {locationName}</div>
          )}

          <div className="avatar-section">
            <p className="avatar-title">Choose your avatar:</p>
            <div className="avatar-picker">
              {[0, 1, 2, 3, 4, 5, 6].map((index) => (
                <button
                  key={index}
                  type="button"
                  className={`avatar-option ${avatarIndex === index ? "selected" : ""}`}
                  onClick={() => {
                    setAvatarIndex(index);
                  }}
                  disabled={loading}
                >
                  <div className="avatar-option-inner">
                    <FoodAvatar avatar_index={index} size={52} />
                  </div>
                </button>
              ))}
            </div>
          </div>

          {error && (
            <span
              style={{
                color: "#D32F2F",
                fontSize: "14px",
                marginTop: "-4px",
                marginBottom: "4px",
              }}
            >
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
