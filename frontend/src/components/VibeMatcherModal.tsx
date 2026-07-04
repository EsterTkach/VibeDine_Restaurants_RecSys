import { useState } from "react";
import type {
  MatchingCategory,
  BudgetOption,
  DistanceOption,
  AccessibilityOption,
  DietaryOption,
  DineOption,
} from "../types/index";
import "./VibeMatcherModal.css";

interface VibeMatcherModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (filters: any) => void;
}

export default function VibeMatcherModal({
  isOpen,
  onClose,
  onSubmit,
}: VibeMatcherModalProps) {
  const [selectedCategories, setSelectedCategories] = useState<
    MatchingCategory[]
  >([]);

  // Preference selections
  const [budgetOption, setBudgetOption] = useState<BudgetOption | null>(null);
  const [distanceOption, setDistanceOption] = useState<DistanceOption | null>(
    null
  );
  const [accessibilityOption, setAccessibilityOption] = useState<AccessibilityOption | null>(null);
  const [dietaryOption, setDietaryOption] = useState<DietaryOption | null>(null);
  const [dineOption, setDineOption] = useState<DineOption | null>(null);

  const budgetOptions: BudgetOption[] = ["$", "$$", "$$$"];
  const distanceOptions: DistanceOption[] = [
    "Walking Distance",
    "Up to 15 Minutes",
    "Up to 30 Minutes",
    "Anywhere",
  ];
  const accessibilityOptions: AccessibilityOption[] = [
    "Required",
    "Not Required",
  ];
  const dietaryOptions: DietaryOption[] = [
    "None",
    "Vegetarian",
    "Vegan",
    "Gluten Free",
  ];
  const dineOptions: DineOption[] = ["Dine-in", "Takeout", "Both"];

  const categories: { key: MatchingCategory; label: string; emoji: string }[] =
    [
      { key: "italian", label: "Italian", emoji: "🍝" },
      { key: "japanese", label: "Japanese", emoji: "🍱" },
      { key: "mexican", label: "Mexican", emoji: "🌮" },
      { key: "thai", label: "Thai", emoji: "🍜" },
      { key: "indian", label: "Indian", emoji: "🍛" },
      { key: "french", label: "French", emoji: "🥐" },
      { key: "korean", label: "Korean", emoji: "🥘" },
      { key: "datenight", label: "Date Night", emoji: "💕" },
      { key: "groups", label: "Groups", emoji: "👥" },
      { key: "coffee", label: "Morning Coffee", emoji: "☕" },
      { key: "lunch", label: "Quick Lunch", emoji: "⏱️" },
      { key: "dessert", label: "Dessert Spot", emoji: "🍰" },
    ];

  const toggleCategory = (cat: MatchingCategory) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

  const buildVibeFilters = () => {
  return {
    categories: selectedCategories.length
      ? selectedCategories.map((category: string) => `${category} restaurant`)
      : null,

    price: budgetOption || null,

    accessibility:
      accessibilityOption === "Required"
        ? ["Wheelchair accessible entrance"]
        : null,

    offerings:
      dietaryOption && dietaryOption !== "None"
        ? [dietaryOption]
        : null,

    service_options:
      dineOption === "Takeout"
        ? ["Takeout"]
        : dineOption === "Dine-in"
        ? ["Dine-in"]
        : null,

    radius_km:
      distanceOption === "Walking Distance"
        ? 2
        : distanceOption === "Up to 15 Minutes"
        ? 8
        : distanceOption === "Up to 30 Minutes"
        ? 16
        : null,

    top_k: 5,
  };
};

  const hasAnySelection =
    budgetOption ||
    distanceOption ||
    accessibilityOption ||
    dietaryOption ||
    dineOption ||
    selectedCategories.length > 0;

  if (!isOpen) return null;

  return (
    <div className="vibe-modal-overlay" onClick={onClose}>
      <div className="vibe-modal-container" onClick={(e) => e.stopPropagation()}>
        {/* Close Button */}
        <button className="vibe-modal-close" onClick={onClose}>
          ✕
        </button>

        {/* Header */}
        <div className="vibe-modal-header">
          <h2>✨ Vibe Matcher</h2>
          <p>Tell us what you're in the mood for</p>
        </div>

        {/* Scrollable Content */}
        <div className="vibe-modal-content">
          {/* Preferences Section */}
          <div className="vibe-section">
            <h3>Preferences</h3>

            {/* Budget */}
            <div className="preference-group">
              <label>💰 Budget</label>
              <div className="segmented-control">
                {budgetOptions.map((option) => (
                  <button
                    key={option}
                    className={`segment ${budgetOption === option ? "active" : ""}`}
                    onClick={() => setBudgetOption(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* Distance */}
            <div className="preference-group">
              <label>📍 Distance</label>
              <div className="segmented-control">
                {distanceOptions.map((option) => (
                  <button
                    key={option}
                    className={`segment ${distanceOption === option ? "active" : ""}`}
                    onClick={() => setDistanceOption(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* Accessibility */}
            <div className="preference-group">
              <label>♿ Accessibility</label>
              <div className="segmented-control">
                {accessibilityOptions.map((option) => (
                  <button
                    key={option}
                    className={`segment ${
                      accessibilityOption === option ? "active" : ""
                    }`}
                    onClick={() => setAccessibilityOption(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* Dietary Restrictions */}
            <div className="preference-group">
              <label>🥗 Dietary Restrictions</label>
              <div className="segmented-control">
                {dietaryOptions.map((option) => (
                  <button
                    key={option}
                    className={`segment ${dietaryOption === option ? "active" : ""}`}
                    onClick={() => setDietaryOption(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* Dine-in / Takeout */}
            <div className="preference-group">
              <label>🍽️ Dine-in / Takeout</label>
              <div className="segmented-control">
                {dineOptions.map((option) => (
                  <button
                    key={option}
                    className={`segment ${dineOption === option ? "active" : ""}`}
                    onClick={() => setDineOption(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Categories Section */}
          <div className="vibe-section">
            <h3>Matching Categories</h3>
            <div className="vibe-chip-grid">
              {categories.map((cat) => (
                <button
                  key={cat.key}
                  className={`vibe-chip ${
                    selectedCategories.includes(cat.key) ? "selected" : ""
                  }`}
                  onClick={() => toggleCategory(cat.key)}
                >
                  <span className="chip-emoji">{cat.emoji}</span>
                  <span className="chip-label">{cat.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom Button */}
        <div className="vibe-modal-footer">
          <button
            className="vibe-match-btn"
            onClick={() => onSubmit(buildVibeFilters())}
            disabled={!hasAnySelection}
          >
            Vibe Match Me ✨
          </button>
        </div>
      </div>
    </div>
  );
}
