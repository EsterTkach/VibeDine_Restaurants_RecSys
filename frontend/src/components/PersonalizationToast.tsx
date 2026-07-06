import { useLiked } from "../contexts/LikedContext";
import "./PersonalizationToast.css";

export default function PersonalizationToast() {
  const { personalizationToast, dismissPersonalizationToast } = useLiked();

  if (!personalizationToast) return null;

  return (
    <div
      className={`personalization-toast personalization-toast--${personalizationToast.variant}`}
      role="status"
      onClick={dismissPersonalizationToast}
    >
      {personalizationToast.message}
    </div>
  );
}
