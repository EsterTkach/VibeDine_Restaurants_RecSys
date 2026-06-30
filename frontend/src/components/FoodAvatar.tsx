import pizza from "../assets/avatars/cute-pizza.png";
import burger from "../assets/avatars/cute-hamburger.png";
import sushi from "../assets/avatars/cute-sushi.png";
import coffee from "../assets/avatars/cute-coffee.png";

import "./FoodAvatar.css";

const avatars = [pizza, burger, sushi, coffee];

type FoodAvatarProps = {
  userId?: string;
  size?: number;
};

export default function FoodAvatar({
  userId = "default",
  size = 90,
}: FoodAvatarProps) {
  const index =
    userId.split("").reduce((sum, char) => sum + char.charCodeAt(0), 0) %
    avatars.length;

  const avatar = avatars[index];

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
