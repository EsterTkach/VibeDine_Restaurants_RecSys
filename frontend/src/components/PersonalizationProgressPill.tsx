import { PERSONALIZATION_THRESHOLD, useLiked } from "../contexts/LikedContext";
import "./PersonalizationProgressPill.css";

export default function PersonalizationProgressPill() {
  const { augmentedLikesCount, isPersonalized } = useLiked();

  // Persistent progress badge — hides itself once the user has unlocked
  // personalization. The unlock celebration is handled by PersonalizationToast.
  if (isPersonalized) return null;

  const remaining = Math.max(0, PERSONALIZATION_THRESHOLD - augmentedLikesCount);
  const percent = Math.min(
    100,
    Math.round((augmentedLikesCount / PERSONALIZATION_THRESHOLD) * 100),
  );

  return (
    <div className="personalization-progress" role="status" aria-live="polite">
      <div className="personalization-progress__label">
        <span aria-hidden="true">❤️</span>
        <span>
          {augmentedLikesCount}/{PERSONALIZATION_THRESHOLD} likes to unlock
          personalized picks
        </span>
      </div>
      <div className="personalization-progress__track">
        <div
          className="personalization-progress__fill"
          style={{ width: `${percent}%` }}
        />
      </div>
      {remaining > 0 && (
        <p className="personalization-progress__hint">
          Like {remaining} more spot{remaining === 1 ? "" : "s"} and we’ll start
          learning your taste.
        </p>
      )}
    </div>
  );
}
