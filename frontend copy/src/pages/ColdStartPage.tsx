import { useState } from "react";
import AppShell from "../layouts/AppShell";
import "./ColdStartPage.css";

const restaurants = [
  {
    id: 1,
    name: "Din Tai Fung",
    cuisine: "Asian",
    image:
      "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
  },
  {
    id: 2,
    name: "The Cheesecake Factory",
    cuisine: "American",
    image:
      "https://images.unsplash.com/photo-1552566626-52f8b828add9"
  },
  {
    id: 3,
    name: "Olive Garden",
    cuisine: "Italian",
    image:
      "https://images.unsplash.com/photo-1559339352-11d035aa65de"
  }
];

export default function ColdStartPage() {
  const [index, setIndex] = useState(0);

  const currentRestaurant = restaurants[index];

  const nextCard = () => {
    if (index < restaurants.length - 1) {
      setIndex(index + 1);
    }
  };

  return (
    <AppShell>
      <div className="cold-start-page">

        <div className="cold-start-header">

          <h1>Let's get to know you</h1>

          <p>
            Help us understand your taste
          </p>

        </div>

        <div className="restaurant-card">

          <img
            src={currentRestaurant.image}
            alt={currentRestaurant.name}
          />

          <div className="restaurant-info">

            <h2>{currentRestaurant.name}</h2>

            <span>
              {currentRestaurant.cuisine}
            </span>

            <p>
              Have you been here?
            </p>

          </div>

        </div>

        <div className="action-buttons">

          <button
            className="skip-btn"
            onClick={nextCard}
          >
            👎 Skip
          </button>

          <button
            className="love-btn"
            onClick={nextCard}
          >
            ❤️ Love It
          </button>

        </div>

        <div className="progress-indicator">
          {index + 1} / {restaurants.length}
        </div>

      </div>
    </AppShell>
  );
}