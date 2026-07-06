import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import RestaurantCard from "../components/RestaurantCard";
import FoodAvatar from "../components/FoodAvatar";
import apiClient from "../api/client";
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
  const [resolvedImageUrl, setResolvedImageUrl] = useState<string | undefined>(
    location.state?.recommendation?.image_url || undefined
  );

  const [showModal, setShowModal] = useState(false);
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState(false);
  const [feedbackError, setFeedbackError] = useState("");
  const [selectedFriendsAffected, setSelectedFriendsAffected] = useState<string[]>([]);
  const [selectedReason, setSelectedReason] = useState("");

  useEffect(() => {
    if (!currentRecommendation) {
      setResolvedImageUrl(undefined);
      return;
    }

    if (currentRecommendation.image_url) {
      setResolvedImageUrl(currentRecommendation.image_url);
      return;
    }

    let cancelled = false;

    apiClient
      .get(`/restaurants/${currentRecommendation.gmap_id}`)
      .then((res) => {
        if (!cancelled) {
          setResolvedImageUrl(res.data?.image_url || "");
        }
      })
      .catch(() => {
        if (!cancelled) {
          setResolvedImageUrl("");
        }
      });

    return () => {
      cancelled = true;
    };
  }, [currentRecommendation?.gmap_id, currentRecommendation?.image_url]);

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
      setResolvedImageUrl(response.recommendation?.image_url || "");
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

          {currentRecommendation ? (
            <RestaurantCard
              restaurant={{
                gmap_id: currentRecommendation.gmap_id,
                name: currentRecommendation.name,
                cuisine: currentRecommendation.cuisines?.[0] || "",
                avg_rating: currentRecommendation.avg_rating || 0,
                price: (currentRecommendation.price as '$' | '$$' | '$$$' | undefined) ?? '$',
                image_url: resolvedImageUrl || currentRecommendation.image_url || "",
              }}
            />
          ) : null}

          <p>
            {currentRecommendation
              ? "Recommended from collaborative preference patterns across the selected group."
              : "No match was found. This usually happens when group members haven't liked any restaurants yet — try liking a few from the home feed first."}
          </p>

          <div className="member-list">
            <h3>Group Size: {selectedFriends.length + 1}</h3>
            <div className="member-item">
              <FoodAvatar avatar_index={0} size={36} />
              <span>You ({currentUserName})</span>
            </div>
            {selectedFriends.map((f: Friend) => (
              <div key={f.user_id} className="member-item">
                <FoodAvatar avatar_index={f.avatar_index} size={36} />
                <span>{f.name || f.username}</span>
              </div>
            ))}
          </div>

          {currentRecommendation && (
            <button
              className="reject-btn"
              disabled={!sessionId}
              onClick={() => setShowModal(true)}
            >
              This recommendation doesn't work
            </button>
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
