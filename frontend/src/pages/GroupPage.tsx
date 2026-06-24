import { useState } from "react";
import { useNavigate } from "react-router-dom";

import AppShell from "../layouts/AppShell";

import "./GroupPage.css";

const friends = [
  "Aya Rotbart",
  "Ester Tkach",
  "Yuval Hazut",
  "Liora Yacob",
  "Yuval Namir Barr",
];

export default function GroupPage() {
  const navigate = useNavigate();

  const [selectedFriends, setSelectedFriends] =
    useState<string[]>([]);

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
              key={friend}
              className={
                selectedFriends.includes(friend)
                  ? "friend-select selected"
                  : "friend-select"
              }
              onClick={() =>
                toggleFriend(friend)
              }
            >
              <div>
                <strong>{friend}</strong>

                <div className="friend-subtitle">
                  Food Explorer 🍜
                </div>
              </div>

              <div className="friend-icon">
                {selectedFriends.includes(friend)
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

        <button
          className="find-match-btn"
          disabled={
            selectedFriends.length === 0
          }
          onClick={() =>
            navigate("/loading", {
              state: {
                selectedFriends,
                nextPage:
                  "/group-result",
              },
            })
          }
        >
          Find Perfect Match →
        </button>

      </div>
    </AppShell>
  );
}