import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import FoodAvatar from "../components/FoodAvatar";
import { getFriends, searchUsers, addFriend, removeFriend } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import type { Friend } from "../types";

import "./FriendsPage.css";

export default function FriendsPage() {
  const { userData } = useAuth();
  const userId = userData.user_id;

  const [friends, setFriends] = useState<Friend[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Friend[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(true);
  const [addingId, setAddingId] = useState<string | null>(null);
  const [addedId, setAddedId] = useState<string | null>(null);
  const [addError, setAddError] = useState<string | null>(null);
  const [removingId, setRemovingId] = useState<string | null>(null);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    if (!userId) return;
    getFriends(userId)
      .then(setFriends)
      .finally(() => setLoading(false));
  }, [userId]);

  useEffect(() => {
    if (searchQuery.trim().length < 2) {
      setSearchResults([]);
      setHasSearched(false);
      return;
    }
    setSearching(true);
    const timer = setTimeout(async () => {
      try {
        const results = await searchUsers(searchQuery, userId);
        setSearchResults(
          results.filter((r) => !friends.some((f) => f.user_id === r.user_id))
        );
      } catch {
        setSearchResults([]);
      } finally {
        setHasSearched(true);
        setSearching(false);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [searchQuery, friends, userId]);

  async function handleRemoveFriend(friend: Friend) {
    setRemovingId(friend.user_id);
    try {
      await removeFriend(userId, friend.user_id);
      setFriends((prev) => prev.filter((f) => f.user_id !== friend.user_id));
    } catch {
      // silent — friend stays in list if removal fails
    } finally {
      setRemovingId(null);
    }
  }

  async function handleAddFriend(friend: Friend) {
    setAddingId(friend.user_id);
    setAddError(null);
    try {
      await addFriend(userId, friend.user_id);
      setFriends((prev) => [...prev, friend]);
      setSearchResults((prev) => prev.filter((r) => r.user_id !== friend.user_id));
      setAddedId(friend.user_id);
      setTimeout(() => setAddedId(null), 1500);
      setSearchQuery("");
      setHasSearched(false);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to add friend";
      setAddError(msg);
    } finally {
      setAddingId(null);
    }
  }

  return (
    <AppShell>
      <div className="friends-page">
        <h1>Your Friends</h1>
        <p>People you love dining with</p>

        <div className="friends-search">
          <input
            className="friends-search-input"
            type="text"
            placeholder="Search by username..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {addError && (
          <p className="friends-empty" style={{ color: "#c0392b" }}>
            Error: {addError}
          </p>
        )}

        {searchQuery.trim().length >= 2 && (
          <div className="friends-list">
            {searching && (
              <p className="friends-empty friends-searching">Searching...</p>
            )}

            {!searching && searchResults.map((user) => (
              <div key={user.user_id} className="friend-card">
                <FoodAvatar avatar_index={user.avatar_index} size={46} />
                <div style={{ flex: 1 }}>
                  <h3>{user.name || user.username}</h3>
                  <span>@{user.username}</span>
                </div>
                <button
                  className={`add-friend-btn${addedId === user.user_id ? " added" : ""}`}
                  onClick={() => handleAddFriend(user)}
                  disabled={addingId === user.user_id}
                >
                  {addingId === user.user_id
                    ? "Adding..."
                    : addedId === user.user_id
                    ? "✓ Added"
                    : "+ Add"}
                </button>
              </div>
            ))}

            {!searching && hasSearched && searchResults.length === 0 && (
              <p className="friends-empty">No users found for "{searchQuery}"</p>
            )}
          </div>
        )}

        <div className="friends-list">
          {loading && <p className="friends-empty">Loading...</p>}

          {!loading && friends.length === 0 && !searchQuery && (
            <p className="friends-empty">No friends yet. Search to add some!</p>
          )}

          {friends.map((friend) => (
            <div key={friend.user_id} className="friend-card">
              <FoodAvatar avatar_index={friend.avatar_index} size={46} />
              <div style={{ flex: 1 }}>
                <h3>{friend.name || friend.username}</h3>
                <span>Food Explorer 🍜</span>
              </div>
              <button
                className="remove-friend-btn"
                onClick={() => handleRemoveFriend(friend)}
                disabled={removingId === friend.user_id}
              >
                {removingId === friend.user_id ? "..." : "✕"}
              </button>
            </div>
          ))}
        </div>
      </div>

      <BottomNav />
    </AppShell>
  );
}
