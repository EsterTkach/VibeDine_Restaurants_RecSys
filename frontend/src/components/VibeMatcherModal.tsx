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

  const toggleCategory = (cat: MatchingCategory) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

    const categoryFilterMap: Record<MatchingCategory, Partial<any>> = {
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

  const buildVibeFilters = () => {
    const filters: Record<string, any> = {
      top_k: 7,
    };

    const addFilterValues = (key: string, values: string[] | null) => {
      if (!values || values.length === 0) return;
      filters[key] = [...(filters[key] || []), ...values];
    };

    selectedCategories.forEach((category) => {
      const filter = categoryFilterMap[category];

      Object.entries(filter).forEach(([key, value]) => {
        addFilterValues(key, value as string[]);
      });
    });

    if (budgetOption) {
      filters.price = budgetOption;
    }

    if (accessibilityOption === "Required") {
      addFilterValues("accessibility", ["Wheelchair accessible entrance"]);
    }

    if (dietaryOption && dietaryOption !== "None") {
      addFilterValues("offerings", [dietaryOption]);
    }

    if (dineOption === "Takeout") {
      addFilterValues("service_options", ["Takeout"]);
    }

    if (dineOption === "Dine-in") {
      addFilterValues("service_options", ["Dine-in"]);
    }

    if (distanceOption === "Walking Distance") {
      filters.radius_km = 2;
    } else if (distanceOption === "Up to 15 Minutes") {
      filters.radius_km = 8;
    } else if (distanceOption === "Up to 30 Minutes") {
      filters.radius_km = 16;
    }

    return filters;
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
