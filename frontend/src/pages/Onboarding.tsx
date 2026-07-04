import "./Onboarding.css";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { vibeService } from "../api/services";
import { preloadHomeData } from "../api/home";

import { useAuth } from "../contexts/AuthContext";
import {
  ONBOARDING_POPULAR_FOOD_OPTIONS,
  ONBOARDING_CUISINE_OPTIONS,
  ONBOARDING_VIBE_OPTIONS,
  ONBOARDING_ACCESSIBILITY_OPTIONS,
  ONBOARDING_DIETARY_OPTIONS,
} from "../constants/onboardingOptions";

type StepKey = "popular-foods" | "cuisines" | "vibes" | "accessibility" | "dietary" | "summary";

type StepConfig = {
  id: StepKey;
  emoji: string;
  title: string;
  subtitle: string;
  options: readonly string[];
  multiSelect: boolean;
};

const STEPS: StepConfig[] = [
  {
    id: "popular-foods",
    emoji: "🍽️",
    title: "What do you crave most?",
    subtitle: "Pick the dishes that make your taste buds happy.",
    options: ONBOARDING_POPULAR_FOOD_OPTIONS,
    multiSelect: true,
  },
  {
    id: "cuisines",
    emoji: "🌍",
    title: "Which cuisines fit your vibe?",
    subtitle: "Choose the styles you love to explore.",
    options: ONBOARDING_CUISINE_OPTIONS,
    multiSelect: true,
  },
  {
    id: "vibes",
    emoji: "✨",
    title: "What atmosphere feels right?",
    subtitle: "Pick the mood that matches your ideal night out.",
    options: ONBOARDING_VIBE_OPTIONS,
    multiSelect: true,
  },
  {
    id: "accessibility",
    emoji: "♿",
    title: "Accessibility needs",
    subtitle: "Let us know if you need an accessible spot.",
    options: ONBOARDING_ACCESSIBILITY_OPTIONS,
    multiSelect: false,
  },
  {
    id: "dietary",
    emoji: "🥗",
    title: "Any dietary preferences?",
    subtitle: "Choose what works best for your plate.",
    options: ONBOARDING_DIETARY_OPTIONS,
    multiSelect: false,
  },
  {
    id: "summary",
    emoji: "🎉",
    title: "We’ve got your vibe",
    subtitle: "Review your picks and generate your personalized recommendations.",
    options: [],
    multiSelect: false,
  },
];

export default function Onboarding() {
  const navigate = useNavigate();
  const { userData } = useAuth();
  const userId = userData.user_id;
  const username = userData.username || "there";

  const [isStarted, setIsStarted] = useState(false);
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [selectedPopularFoods, setSelectedPopularFoods] = useState<string[]>([]);
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [selectedVibes, setSelectedVibes] = useState<string[]>([]);
  const [accessibility, setAccessibility] = useState("");
  const [dietary, setDietary] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentStep = useMemo(() => STEPS[activeStepIndex], [activeStepIndex]);
  const hasSelections =
    selectedPopularFoods.length > 0 ||
    selectedCuisines.length > 0 ||
    selectedVibes.length > 0 ||
    Boolean(accessibility) ||
    Boolean(dietary);

  const toggleSelection = (item: string, setList: React.Dispatch<React.SetStateAction<string[]>>) => {
    setList((prev) => (prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]));
  };

  const handleNext = () => {
    if (activeStepIndex < STEPS.length - 1) {
      setActiveStepIndex((prev) => prev + 1);
      return;
    }

    void handleComplete();
  };

  const handleBack = () => {
    if (activeStepIndex > 0) {
      setActiveStepIndex((prev) => prev - 1);
    }
  };

  const handleSkip = () => {
    if (activeStepIndex < STEPS.length - 1) {
      setActiveStepIndex((prev) => prev + 1);
    } else {
      void handleComplete();
    }
  };

  const handleComplete = async () => {
    if (!userId) {
      navigate("/login", { replace: true });
      return;
    }

    const userPreferences = {
      favorite_categories: [...new Set([...selectedPopularFoods, ...selectedCuisines])],
      favorite_atmospheres: selectedVibes,
      accessibility: accessibility || "Not Required",
      dietary_restrictions: dietary || "None",
    };

    setIsSubmitting(true);

    try {
      await vibeService.submitMatch(userId, userPreferences);
    } catch (error) {
      console.warn("Backend offline. Simulating local onboarding preferences save...", error);
    } finally {
      preloadHomeData(userId);
      navigate("/loading", {
        state: {
          nextPage: "/home",
          username: userData.username,
          user_id: userId,
        },
        replace: true,
      });
      setIsSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="onboarding-page">
        <div className="welcome-card">
          <div className="welcome-badge">🍽️ VibeDine</div>
          <div className="welcome-emojis">🍕 🍣 🥗 🍔 🍰</div>
          <h1>Welcome{username ? `, ${username}` : ""}!</h1>
          <p className="welcome-subtitle">
            Let’s build your perfect dining match with your favorite flavors, vibes, and accessibility needs.
          </p>
        </div>

        <div className="welcome-action">
          <button className="submit-btn welcome-start" onClick={() => setIsStarted(true)}>
            Build My Perfect Match →
          </button>
        </div>

        {isStarted && (
          <div className="onboarding-overlay" role="dialog" aria-modal="true">
            <div className="onboarding-modal">
              <div className="modal-progress">
                {STEPS.map((step, index) => (
                  <span key={step.id} className={`progress-dot ${index <= activeStepIndex ? "active" : ""}`} />
                ))}
              </div>

              <div className="modal-header">
                <h2>
                  {currentStep.emoji} {currentStep.title}
                </h2>
                <p>{currentStep.subtitle}</p>
              </div>

              {currentStep.id === "summary" ? (
                <div className="summary-card">
                  <p>Your picks so far:</p>
                  <ul>
                    {selectedPopularFoods.length > 0 && <li>Favorite foods: {selectedPopularFoods.join(", ")}</li>}
                    {selectedCuisines.length > 0 && <li>Cuisines: {selectedCuisines.join(", ")}</li>}
                    {selectedVibes.length > 0 && <li>Vibes: {selectedVibes.join(", ")}</li>}
                    {accessibility && <li>Accessibility: {accessibility}</li>}
                    {dietary && <li>Dietary: {dietary}</li>}
                    {!hasSelections && <li>No preferences picked yet — that is totally okay.</li>}
                  </ul>
                </div>
              ) : currentStep.multiSelect ? (
                <div className="segmented-control">
                  {currentStep.options.map((option) => {
                    const isActive =
                      currentStep.id === "popular-foods"
                        ? selectedPopularFoods.includes(option)
                        : currentStep.id === "cuisines"
                          ? selectedCuisines.includes(option)
                          : selectedVibes.includes(option);

                    return (
                      <button
                        key={option}
                        className={isActive ? "segment active" : "segment"}
                        onClick={() => {
                          if (currentStep.id === "popular-foods") {
                            toggleSelection(option, setSelectedPopularFoods);
                          } else if (currentStep.id === "cuisines") {
                            toggleSelection(option, setSelectedCuisines);
                          } else {
                            toggleSelection(option, setSelectedVibes);
                          }
                        }}
                      >
                        {option}
                      </button>
                    );
                  })}
                </div>
              ) : (
                <div className="segmented-control single-select">
                  {currentStep.options.map((option) => (
                    <button
                      key={option}
                      className={
                        (currentStep.id === "accessibility" ? accessibility : dietary) === option
                          ? "segment active"
                          : "segment"
                      }
                      onClick={() => {
                        if (currentStep.id === "accessibility") {
                          setAccessibility(option);
                        } else {
                          setDietary(option);
                        }
                      }}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              )}

              <div className="modal-actions">
                {activeStepIndex > 0 && (
                  <button className="ghost-btn" onClick={handleBack}>
                    Back
                  </button>
                )}

                <button className="ghost-btn" onClick={handleSkip}>
                  {activeStepIndex === STEPS.length - 1 ? "Skip" : "Skip this"}
                </button>

                <button className="submit-btn modal-submit" onClick={handleNext} disabled={isSubmitting}>
                  {activeStepIndex === STEPS.length - 1
                    ? "Generate Recommendations That Match My Vibe"
                    : "Next"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}