import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { createGroupSession } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import AppShell from "../layouts/AppShell";

import "./GroupPage.css";

const friends = [
  {
    id: "ester_tkach",
    name: "Ester Tkach",
  },
  {
    id: "yuval_hazut",
    name: "Yuval Hazut",
  },
  {
    id: "liora_yacob",
    name: "Liora Yacob",
  },
  {
    id: "yuval_namir_barr",
    name: "Yuval Namir Barr",
  },
];

export default function GroupPage() {
  const navigate = useNavigate();
  const { userId, username } = useAuth();

  const [selectedFriends, setSelectedFriends] =
    useState<string[]>([]);
  const [isCreatingSession, setIsCreatingSession] =
    useState(false);
  const [error, setError] = useState("");

const [budget, setBudget] = useState("");

const [distance, setDistance] =
  useState("");

const [accessibility, setAccessibility] =
  useState("");

const [dietary, setDietary] =
  useState("");

  const toggleFriend = (friend: string) => {
    setSelectedFriends((prev) =>
      prev.includes(friend)
        ? prev.filter((f) => f !== friend)
        : [...prev, friend]
    );
  };

  const handleFindMatch = async () => {
    setIsCreatingSession(true);
    setError("");

    try {
      const currentUserId = userId || "default_user_id";
      const selectedFriendProfiles = friends.filter((friend) =>
        selectedFriends.includes(friend.name)
      );
      const groupUserIds = [
        currentUserId,
        ...selectedFriendProfiles.map((friend) => friend.id),
      ];

      const session = await createGroupSession(groupUserIds);

      navigate("/loading", {
        state: {
          selectedFriends,
          currentUserId,
          currentUserName: username || "You",
          friendUserIdsByName: Object.fromEntries(
            selectedFriendProfiles.map((friend) => [friend.name, friend.id])
          ),
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

        <h1>Plan With Friends</h1>

        <p>
          Select the people joining you
        </p>

        <div className="friends-selection">

          {friends.map((friend) => (
            <button
              key={friend.id}
              className={
                selectedFriends.includes(friend.name)
                  ? "friend-select selected"
                  : "friend-select"
              }
              onClick={() =>
                toggleFriend(friend.name)
              }
            >
              <div>
                <strong>{friend.name}</strong>

                <div className="friend-subtitle">
                  Food Explorer 🍜
                </div>
              </div>

              <div className="friend-icon">
                {selectedFriends.includes(friend.name)
                  ? "✓"
                  : "+"}
              </div>
            </button>
          ))}

        </div>

        <div className="filters">

          <h3>Group Preferences</h3>

          <div className="preference-group">
            <label>💰 Budget</label>

            <div className="segmented-control">
              {["$", "$$", "$$$", "$$$$"].map(
                (value) => (
                  <button
                    key={value}
                    className={
                      budget === value
                        ? "segment active"
                        : "segment"
                    }
                    onClick={() =>
                      setBudget(value)
                    }
                  >
                    {value}
                  </button>
                )
              )}
            </div>
          </div>

          <div className="preference-group">
            <label>📍 Distance</label>

            <div className="segmented-control">
              {[
                "Walkable",
                "15 Min",
                "30 Min",
                "Anywhere",
              ].map((value) => (
                <button
                  key={value}
                  className={
                    distance === value
                      ? "segment active"
                      : "segment"
                  }
                  onClick={() =>
                    setDistance(value)
                  }
                >
                  {value}
                </button>
              ))}
            </div>
          </div>

          <div className="preference-group">
            <label>♿ Accessibility</label>

            <div className="segmented-control">
              {[
                "Required",
                "Not Required",
              ].map((value) => (
                <button
                  key={value}
                  className={
                    accessibility === value
                      ? "segment active"
                      : "segment"
                  }
                  onClick={() =>
                    setAccessibility(value)
                  }
                >
                  {value}
                </button>
              ))}
            </div>
          </div>

          <div className="preference-group">
            <label>🥗 Dietary</label>

            <div className="segmented-control">
              {[
                "None",
                "Vegetarian",
                "Vegan",
                "Gluten Free",
              ].map((value) => (
                <button
                  key={value}
                  className={
                    dietary === value
                      ? "segment active"
                      : "segment"
                  }
                  onClick={() =>
                    setDietary(value)
                  }
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
          disabled={
            selectedFriends.length === 0 || isCreatingSession
          }
          onClick={handleFindMatch}
        >
          {isCreatingSession ? "Finding..." : "Find Perfect Match →"}
        </button>

      </div>
    </AppShell>
  );
}
