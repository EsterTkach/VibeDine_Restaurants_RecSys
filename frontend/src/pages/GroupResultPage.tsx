import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

import AppShell from "../layouts/AppShell";

import "./GroupResultPage.css";

export default function GroupResultPage() {

  const [showBanner, setShowBanner] =
  useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const selectedFriends =
    location.state?.selectedFriends || [];

  const [showModal, setShowModal] = useState(false);

  const [
    selectedFriendsAffected,
    setSelectedFriendsAffected,
  ] = useState<string[]>([]);

  const toggleAffectedFriend = (
    friend: string
  ) => {

    setSelectedFriendsAffected(
      (prev) =>

        prev.includes(friend)

          ? prev.filter(
              (f) => f !== friend
            )

          : [...prev, friend]
    );

  };

  const [selectedReason, setSelectedReason] =
    useState("");

  const handleSubmitFeedback = () => {
    setShowBanner(true);

    setTimeout(() => {

      navigate("/loading", {
        state: {
          selectedFriends,
          nextPage: "/group-result",
        },
      });

    }, 2500);

  };

  return (
    <AppShell>
      <div className="group-result-page">
        {showBanner && (
          <div className="working-banner">
            🚀 We're working on it
          </div>
        )}
        {showModal && (
          <div className="feedback-overlay">

            <div className="feedback-modal">

              <h2>
                Why doesn't this recommendation work?
              </h2>

              <p>
                Help us improve the group's
                recommendation.
              </p>

              <div className="feedback-section">

                <h4>Who is affected?</h4>

                {[
                  "You (Aya Rotbart)",
                  ...selectedFriends,
                ].map((friend) => (

                  <button
                    key={friend}
                    className={
                      selectedFriendsAffected.includes(friend)
                        ? "feedback-option active"
                        : "feedback-option"
                    }
                    onClick={() =>
                      toggleAffectedFriend(friend)
                    }
                  >
                    {friend}
                  </button>

                ))}

              </div>

              <div className="feedback-section">

                <h4>Reason</h4>

                {[
                  "Doesn't like this restaurant",
                  "We visited recently",
                  "Too expensive",
                  "Too far away",
                  "Other",
                ].map((reason) => (

                  <button
                    key={reason}
                    className={
                      selectedReason === reason
                        ? "feedback-option active"
                        : "feedback-option"
                    }
                    onClick={() =>
                      setSelectedReason(reason)
                    }
                  >
                    {reason}
                  </button>

                ))}

              </div>

              <button
                className="reserve-btn"
                disabled={
                  !selectedFriendsAffected.length ||
                  !selectedReason
                }
                onClick={handleSubmitFeedback}
              >
                Find A Better Match →
              </button>

              <button
                className="close-feedback"
                onClick={() =>
                  setShowModal(false)
                }
              >
                Cancel
              </button>

            </div>

          </div>
        )}

        <div className="result-content">

          <button
            className="back-btn"
            onClick={() => navigate("/group")}
          >
            ← Back
          </button>

          <span className="recommendation-badge">
            Top Group Recommendation
          </span>

          <h1>Nobu</h1>

          <p>
            Recommended from collaborative
            preference patterns across
            the selected group.
          </p>

          <div className="member-list">

            <h3>
              Group Size:{" "}
              {selectedFriends.length + 1}
            </h3>

            <span>
              You (Aya Rotbart)
            </span>

            {selectedFriends.map(
              (friend: string) => (
                <span key={friend}>
                  {friend}
                </span>
              )
            )}

          </div>

          <button className="reserve-btn">
            View Restaurant →
          </button>

          <button
            className="reject-btn"
            onClick={() =>
              setShowModal(true)
            }
          >
            This recommendation doesn't work
          </button>

        </div>

      </div>
    </AppShell>
  );
}