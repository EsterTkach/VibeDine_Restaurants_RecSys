import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import RestaurantDetailPage from './pages/RestaurantDetailPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}
