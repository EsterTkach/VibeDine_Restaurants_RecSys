import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import LoadingPage from "./pages/LoadingPage";
import SignUpPage from "./pages/SignUpPage";
import HomePage from "./pages/HomePage";
import FriendsPage from "./pages/FriendsPage";
import ProfilePage from "./pages/ProfilePage";
import GroupPage from "./pages/GroupPage";
import GroupResultPage from "./pages/GroupResultPage";
import RestaurantPage from "./pages/RestaurantPage";
import Onboarding from "./pages/Onboarding";
import VibeMatchPage from "./pages/VibeMatchPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/login" element={<AuthPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/loading" element={<LoadingPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/friends" element={<FriendsPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/restaurant" element={<RestaurantPage />} />
        <Route path="/group" element={<GroupPage />} />
        <Route path="/group-result" element={<GroupResultPage />} />
        <Route path="/vibe-match" element={<VibeMatchPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;