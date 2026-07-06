import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { getFriends } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import type { Friend, MatchingCategory } from "../types";

import "./GroupPage.css";

export default function GroupPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { userData } = useAuth();
  const userId  = userData.user_id;
  const username  = userData.username;


  const [friends, setFriends] = useState<Friend[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFriends, setSelectedFriends] = useState<Friend[]>([]);
  const [error, setError] = useState<string>(location.state?.groupError || "");

  const [budget, setBudget] = useState("");
  const [distance, setDistance] = useState("");
  const [accessibility, setAccessibility] = useState("");
  const [dietary, setDietary] = useState("");
  const [selectedFoodTypes, setSelectedFoodTypes] = useState<MatchingCategory[]>([]);

  const foodCategories: { key: MatchingCategory; label: string; emoji: string }[] = [
    { key: "american", label: "American", emoji: "🍔" },
    { key: "italian", label: "Italian", emoji: "🍝" },
    { key: "chinese", label: "Chinese", emoji: "🥡" },
    { key: "mexican_latin", label: "Mexican & Latin", emoji: "🌮" },
    { key: "indian", label: "Indian", emoji: "🍛" },
    { key: "cafe", label: "Cafe", emoji: "☕" },
    { key: "breakfast_brunch", label: "Breakfast & Brunch", emoji: "🥐" },
    { key: "lunch", label: "Lunch", emoji: "🥗" },
    { key: "dinner", label: "Dinner", emoji: "🍽️" },
    { key: "fast_food", label: "Fast Food / Quick Bite", emoji: "⏱️" },
    { key: "vegetarian", label: "Vegetarian", emoji: "🥬" },
    { key: "halal", label: "Halal", emoji: "🌙" },
  ];

  const categoryFilterMap: Record<MatchingCategory, Record<string, string[]>> = {
    american: { categories: ["American"] },
    italian: { categories: ["Italian"] },
    chinese: { categories: ["Chinese"] },
    mexican_latin: { categories: ["Mexican & Latin"] },
    indian: { categories: ["Indian"] },
    cafe: { establishment_types: ["Cafe"] },
    breakfast_brunch: { meal_types: ["Breakfast & Brunch"] },
    lunch: { meal_types: ["Lunch"] },
    dinner: { meal_types: ["Dinner"] },
    fast_food: { dining_styles: ["Fast Food / Quick Bite"] },
    vegetarian: { dietary_preferences: ["Vegetarian"] },
    halal: { dietary_preferences: ["Halal"] },
  };

  const toggleFoodType = (cat: MatchingCategory) => {
    setSelectedFoodTypes((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

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
    if (accessibility === "Required") filters.is_accessible = true;
    if (dietary === "Vegetarian") filters.dietary_preferences = ["Vegetarian"];
    else if (dietary === "Vegan") filters.dietary_preferences = ["Vegan"];
    else if (dietary === "Gluten Free") filters.dietary_preferences = ["Gluten-Free"];
    else if (dietary === "Kosher") filters.dietary_preferences = ["Kosher"];
    else if (dietary === "Halal") filters.dietary_preferences = ["Halal"];

    // Map selected food types to their respective filter fields
    selectedFoodTypes.forEach((cat) => {
      const mapping = categoryFilterMap[cat];
      Object.entries(mapping).forEach(([key, values]) => {
        const existing = (filters[key] as string[]) || [];
        filters[key] = [...existing, ...values];
      });
    });

    return filters;
  };

  const handleFindMatch = () => {
    setError("");
    const groupUserIds = [userId, ...selectedFriends.map((f) => f.user_id)];
    navigate("/loading", {
      state: {
        selectedFriends,
        currentUserId: userId,
        currentUserName: username || "You",
        groupUserIds,
        groupFilters: buildFilters(),
        mode: "group",
        nextPage: "/group-result",
      },
    });
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
                <label>🍽️ Food Type</label>
                <div className="segmented-control">
                  {foodCategories.map(({ key, label, emoji }) => (
                    <button
                      key={key}
                      className={selectedFoodTypes.includes(key) ? "segment active" : "segment"}
                      onClick={() => toggleFoodType(key)}
                    >
                      {emoji} {label}
                    </button>
                  ))}
                </div>
              </div>

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
              disabled={selectedFriends.length === 0}
              onClick={handleFindMatch}
            >
              Find Perfect Match →
            </button>
          </>
        )}

      </div>
    </AppShell>
  );
}
