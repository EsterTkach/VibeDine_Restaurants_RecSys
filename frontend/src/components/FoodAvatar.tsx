import pizza from "../assets/avatars/cute-pizza.png";
import burger from "../assets/avatars/cute-hamburger.png";
import sushi from "../assets/avatars/cute-sushi.png";
import coffee from "../assets/avatars/cute-coffee.png";
import avocado from "../assets/avatars/cute-avocado-1.png";
import cupcake from "../assets/avatars/cute-cupcake.png";
import burrito from "../assets/avatars/cute-burrito.png";
import cocktail from "../assets/avatars/cute-cocktail.png";
import beer from "../assets/avatars/cute-beer.png";

import "./FoodAvatar.css";

const avatars = [pizza, burger, sushi, avocado, cupcake, beer, coffee];

type FoodAvatarProps = {
  avatar_index?: number;
  size?: number;
};

export default function FoodAvatar({ avatar_index = 0, size = 90 }: FoodAvatarProps) {
  const avatar = avatars[avatar_index];

  return (
    <div
      className="food-avatar"
      style={{
        width: size,
        height: size,
      }}
    >
      <img src={avatar} alt="Food avatar" />
    </div>
  );
}
