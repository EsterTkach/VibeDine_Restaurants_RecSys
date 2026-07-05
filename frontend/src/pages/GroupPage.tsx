import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { getFriends, createGroupSession } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import type { Friend } from "../types";

import "./GroupPage.css";

export default function GroupPage() {
  const navigate = useNavigate();
  const { userData } = useAuth();
  const userId  = userData.user_id;
  const username  = userData.username;


  const [friends, setFriends] = useState<Friend[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFriends, setSelectedFriends] = useState<Friend[]>([]);
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [error, setError] = useState("");

  const [budget, setBudget] = useState("");
  const [distance, setDistance] = useState("");
  const [accessibility, setAccessibility] = useState("");
  const [dietary, setDietary] = useState("");

  useEffect(() => {
    if (!userId) return;
    getFriends(userId)
      .then(setFriends)
      .finally(() => setLoading(false));
  }, [userId]);

  const toggleFriend = (friend: Friend) => {
    setSelectedFriends((prev) =>
      prev.some((f) => f.user_id === friend.user_id)
        ? prev.filter((f) => f.user_id !== friend.user_id)
        : [...prev, friend]
    );
  };

  const isSelected = (friend: Friend) =>
    selectedFriends.some((f) => f.user_id === friend.user_id);

  const hasFriends = !loading && friends.length > 0;
  const noFriends = !loading && friends.length === 0;

  const buildFilters = (): Record<string, unknown> => {
    const filters: Record<string, unknown> = {};
    if (budget) filters.price = budget;
    if (distance === "Walkable") filters.radius_km = 1;
    else if (distance === "15 Min") filters.radius_km = 3;
    else if (distance === "30 Min") filters.radius_km = 6;
    if (accessibility === "Required")
      filters.accessibility = ["Wheelchair accessible entrance", "Wheelchair accessible seating", "Wheelchair accessible"];
    if (dietary === "Vegetarian") filters.dietary_restrictions = ["Vegetarian"];
    else if (dietary === "Vegan") filters.dietary_restrictions = ["Vegan"];
    else if (dietary === "Gluten Free") filters.dietary_restrictions = ["Gluten-Free"];
    else if (dietary === "Kosher") filters.dietary_restrictions = ["Kosher"];
    else if (dietary === "Halal") filters.dietary_restrictions = ["Halal"];
    return filters;
  };

  const handleFindMatch = async () => {
    setIsCreatingSession(true);
    setError("");
    try {
      const groupUserIds = [userId, ...selectedFriends.map((f) => f.user_id)];
      const session = await createGroupSession(groupUserIds, buildFilters());
      navigate("/loading", {
        state: {
          selectedFriends,
          currentUserId: userId,
          currentUserName: username || "You",
          groupUserIds,
          groupSessionId: session.session_id,
          recommendation: session.recommendation,
          nextPage: "/group-result",
        },
      });
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.message || "Unknown error";
      console.error("Group session error:", detail, err?.response?.status);
      setError(`Could not start a group session: ${detail}`);
    } finally {
      setIsCreatingSession(false);
    }
  };

  return (
    <AppShell>
      <div className="group-page">

        <button className="back-btn" onClick={() => navigate("/home")}>
          ← Back
        </button>

        <h1>Plan With Friends</h1>
        <p>Select the people joining you</p>

        {noFriends && (
          <div className="group-empty-state">
            <div className="group-empty-icon">👥</div>
            <h2>No friends yet</h2>
            <p>Add friends from the Friends page to use this feature!</p>
            <button className="go-friends-btn" onClick={() => navigate("/friends")}>
              Go to Friends
            </button>
          </div>
        )}

        {loading && (
          <p style={{ color: "#aaa", fontSize: 14, marginTop: 24 }}>Loading...</p>
        )}

        {hasFriends && (
          <>
            <div className="friends-selection">
              {friends.map((friend) => (
                <button
                  key={friend.user_id}
                  className={isSelected(friend) ? "friend-select selected" : "friend-select"}
                  onClick={() => toggleFriend(friend)}
                >
                  <div>
                    <strong>{friend.name || friend.username}</strong>
                    <div className="friend-subtitle">Food Explorer 🍜</div>
                  </div>
                  <div className="friend-icon">
                    {isSelected(friend) ? "✓" : "+"}
                  </div>
                </button>
              ))}
            </div>

            <div className="filters">
              <h3>Group Preferences</h3>

              <div className="preference-group">
                <label>💰 Budget</label>
                <div className="segmented-control">
                  {["$", "$$", "$$$", "$$$$"].map((value) => (
                    <button
                      key={value}
                      className={budget === value ? "segment active" : "segment"}
                      onClick={() => setBudget(value)}
                    >
                      {value}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <label>📍 Distance</label>
                <div className="segmented-control">
                  {["Walkable", "15 Min", "30 Min", "Anywhere"].map((value) => (
                    <button
                      key={value}
                      className={distance === value ? "segment active" : "segment"}
                      onClick={() => setDistance(value)}
                    >
                      {value}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <label>♿ Accessibility</label>
                <div className="segmented-control">
                  {["Required", "Not Required"].map((value) => (
                    <button
                      key={value}
                      className={accessibility === value ? "segment active" : "segment"}
                      onClick={() => setAccessibility(value)}
                    >
                      {value}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <label>🥗 Dietary</label>
                <div className="segmented-control">
                  {["None", "Vegetarian", "Vegan", "Kosher", "Halal", "Gluten Free"].map((value) => (
                    <button
                      key={value}
                      className={dietary === value ? "segment active" : "segment"}
                      onClick={() => setDietary(value)}
                    >
                      {value}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {error && <p className="group-error">{error}</p>}

            <button
              className="find-match-btn"
              disabled={selectedFriends.length === 0 || isCreatingSession}
              onClick={handleFindMatch}
            >
              {isCreatingSession ? "Finding..." : "Find Perfect Match →"}
            </button>
          </>
        )}

      </div>
    </AppShell>
  );
}
