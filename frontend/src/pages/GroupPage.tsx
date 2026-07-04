import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { getFriends, createGroupSession } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import type { Friend } from "../types";

import "./GroupPage.css";

export default function GroupPage() {
  const navigate = useNavigate();
  const { userId, username } = useAuth();

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

  const handleFindMatch = async () => {
    setIsCreatingSession(true);
    setError("");
    try {
      const groupUserIds = [userId, ...selectedFriends.map((f) => f.user_id)];
      const session = await createGroupSession(groupUserIds);
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
    } catch (err) {
      setError("Could not start a group session. Please try again.");
    } finally {
      setIsCreatingSession(false);
    }
  };

  return (
    <AppShell>
      <div className="group-page">

        <button className="back-btn" onClick={() => navigate(-1)}>
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
                  {["None", "Vegetarian", "Vegan", "Gluten Free"].map((value) => (
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
