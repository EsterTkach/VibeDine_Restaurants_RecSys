import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";

import "./FriendsPage.css";

const friends = [
  "Aya Rotbart",
  "Ester Tkach",
  "Yuval Hazut",
  "Liora Yacob",
  "Yuval Namir Barr",
];

export default function FriendsPage() {
  return (
    <AppShell>

      <div className="friends-page">

        <h1>Your Friends</h1>

        <p>
          People you love dining with
        </p>

        <div className="friends-list">

          {friends.map((friend) => (
            <div
              key={friend}
              className="friend-card"
            >
              <div className="friend-avatar">
                {friend[0]}
              </div>

              <div>
                <h3>{friend}</h3>

                <span>
                  Food Explorer 🍜
                </span>
              </div>
            </div>
          ))}

        </div>

      </div>

      <BottomNav />

    </AppShell>
  );
}