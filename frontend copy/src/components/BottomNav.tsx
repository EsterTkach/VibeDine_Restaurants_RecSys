import { useLocation, useNavigate } from "react-router-dom";
import { FaHouse, FaUser, FaUserGroup } from "react-icons/fa6";

import "./BottomNav.css";

export default function BottomNav() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="bottom-nav">

      <button
        className={
          location.pathname === "/home"
            ? "nav-item active"
            : "nav-item"
        }
        onClick={() => navigate("/home")}
      >
        <FaHouse />
        <span>Home</span>
      </button>

      <button
        className={
          location.pathname === "/friends"
            ? "nav-item active"
            : "nav-item"
        }
        onClick={() => navigate("/friends")}
      >
        <FaUserGroup />
        <span>Friends</span>
      </button>

      <button
        className={
          location.pathname === "/profile"
            ? "nav-item active"
            : "nav-item"
        }
        onClick={() => navigate("/profile")}
      >
        <FaUser />
        <span>Profile</span>
      </button>

    </div>
  );
}