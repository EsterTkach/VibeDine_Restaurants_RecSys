import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

import {
  submitGroupSessionFeedback,
  type GroupRecommendation,
} from "../api/restaurants";
import type { Friend } from "../types";
import AppShell from "../layouts/AppShell";

import "./GroupResultPage.css";

export default function GroupResultPage() {
  const [showBanner, setShowBanner] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const selectedFriends: Friend[] = location.state?.selectedFriends || [];
  const sessionId = location.state?.groupSessionId || "";
  const currentUserId = location.state?.currentUserId || "default_user_id";
  const currentUserName = location.state?.currentUserName || "You";

  const [currentRecommendation, setCurrentRecommendation] =
    useState<GroupRecommendation | null>(location.state?.recommendation || null);

  const [showModal, setShowModal] = useState(false);
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState(false);
  const [feedbackError, setFeedbackError] = useState("");
  const [selectedFriendsAffected, setSelectedFriendsAffected] = useState<string[]>([]);
  const [selectedReason, setSelectedReason] = useState("");

  const toggleAffectedFriend = (label: string) => {
    setSelectedFriendsAffected((prev) =>
      prev.includes(label) ? prev.filter((f) => f !== label) : [...prev, label]
    );
  };

  const affectedOptions = [
    { label: `You (${currentUserName})`, userId: currentUserId },
    ...selectedFriends.map((f: Friend) => ({
      label: f.name || f.username,
      userId: f.user_id,
    })),
  ];

  const handleSubmitFeedback = async () => {
    if (!sessionId || !currentRecommendation) {
      setFeedbackError("Missing group session. Please start again.");
      return;
    }

    setIsSubmittingFeedback(true);
    setFeedbackError("");

    try {
      const affectedUserIds = affectedOptions
        .filter((option) => selectedFriendsAffected.includes(option.label))
        .map((option) => option.userId)
        .filter((userId): userId is string => Boolean(userId));

      const response = await submitGroupSessionFeedback(
        sessionId,
        currentRecommendation.gmap_id,
        affectedUserIds,
        selectedReason
      );

      setCurrentRecommendation(response.recommendation);
      setSelectedFriendsAffected([]);
      setSelectedReason("");
      setShowModal(false);
      setShowBanner(true);
      setTimeout(() => setShowBanner(false), 1800);
    } catch (err) {
      setFeedbackError("Could not find a better match. Please try again.");
    } finally {
      setIsSubmittingFeedback(false);
    }
  };

  return (
    <AppShell>
      <div className="group-result-page">
        {showBanner && (
          <div className="working-banner">Updated the group recommendation</div>
        )}

        {showModal && (
          <div className="feedback-overlay">
            <div className="feedback-modal">
              <h2>Why doesn't this recommendation work?</h2>
              <p>Help us improve the group's recommendation.</p>

              <div className="feedback-section">
                <h4>Who is affected?</h4>
                {affectedOptions.map((option) => (
                  <button
                    key={option.label}
                    className={
                      selectedFriendsAffected.includes(option.label)
                        ? "feedback-option active"
                        : "feedback-option"
                    }
                    onClick={() => toggleAffectedFriend(option.label)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>

              <div className="feedback-section">
                <h4>Reason</h4>
                {["Doesn't like this restaurant", "Too expensive", "Too far away", "Other"].map(
                  (reason) => (
                    <button
                      key={reason}
                      className={
                        selectedReason === reason ? "feedback-option active" : "feedback-option"
                      }
                      onClick={() => setSelectedReason(reason)}
                    >
                      {reason}
                    </button>
                  )
                )}
              </div>

              <button
                className="reserve-btn"
                disabled={
                  !selectedFriendsAffected.length || !selectedReason || isSubmittingFeedback
                }
                onClick={handleSubmitFeedback}
              >
                {isSubmittingFeedback ? "Finding..." : "Find A Better Match →"}
              </button>

              {feedbackError && <p className="feedback-error">{feedbackError}</p>}

              <button className="close-feedback" onClick={() => setShowModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        )}

        <div className="result-content">
          <button className="close-result-btn" onClick={() => navigate("/home")}>
            ✕
          </button>

          <span className="recommendation-badge">Top Group Recommendation</span>

          <h1>{currentRecommendation?.name || "No match found"}</h1>

          {currentRecommendation?.image_url && (
            <img
              src={currentRecommendation.image_url}
              className="result-restaurant-img"
              alt={currentRecommendation.name}
            />
          )}

          <div className="result-meta">
            {currentRecommendation?.avg_rating && (
              <span>⭐ {currentRecommendation.avg_rating}</span>
            )}
            {currentRecommendation?.price && (
              <span>• {currentRecommendation.price}</span>
            )}
            {currentRecommendation?.cuisines?.[0] && (
              <span>• {currentRecommendation.cuisines[0]}</span>
            )}
          </div>

          <p>
            {currentRecommendation
              ? "Recommended from collaborative preference patterns across the selected group."
              : "No match was found. This usually happens when group members haven't liked any restaurants yet — try liking a few from the home feed first."}
          </p>

          <div className="member-list">
            <h3>Group Size: {selectedFriends.length + 1}</h3>
            <span>You ({currentUserName})</span>
            {selectedFriends.map((f: Friend) => (
              <span key={f.user_id}>{f.name || f.username}</span>
            ))}
          </div>

          {currentRecommendation && (
            <>
              <button
                className="reserve-btn"
                onClick={() => navigate(`/restaurant/${currentRecommendation.gmap_id}`)}
              >
                View Restaurant →
              </button>

              <button
                className="reject-btn"
                disabled={!sessionId}
                onClick={() => setShowModal(true)}
              >
                This recommendation doesn't work
              </button>
            </>
          )}

          {!currentRecommendation && (
            <button className="reserve-btn" onClick={() => navigate("/group")}>
              ← Try Again
            </button>
          )}
        </div>
      </div>
    </AppShell>
  );
}
