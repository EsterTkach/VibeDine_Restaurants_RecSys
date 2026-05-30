import { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import RestaurantCard from '../components/RestaurantCard';
import { MOCK_USER } from '../data/mockData';

type PreferenceKey = 'glutenFree' | 'vegetarian' | 'vegan' | 'dineIn' | 'takeout' | 'laptopFriendly';

const DEFAULT_PREFERENCES: Record<PreferenceKey, boolean> = {
  glutenFree: false, vegetarian: false, vegan: false,
  dineIn: true, takeout: true, laptopFriendly: false,
};

const PREFERENCE_LABELS: Record<PreferenceKey, { label: string; emoji: string }> = {
  glutenFree:     { label: 'Gluten Free',    emoji: '🌾' },
  vegetarian:     { label: 'Vegetarian',     emoji: '🥦' },
  vegan:          { label: 'Vegan',          emoji: '🌱' },
  dineIn:         { label: 'Dine In',        emoji: '🍽️' },
  takeout:        { label: 'Takeout',        emoji: '📦' },
  laptopFriendly: { label: 'Laptop Friendly',emoji: '💻' },
};

export default function ProfilePage() {
  const user = MOCK_USER;
  const [preferences, setPreferences] = useState(DEFAULT_PREFERENCES);
  const [inviteSent, setInviteSent] = useState(false);

  const initials = user.username.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2);

  function togglePref(key: PreferenceKey) {
    setPreferences((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  function handleInvite() {
    setInviteSent(true);
    setTimeout(() => setInviteSent(false), 3000);
  }

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />

      {/* Full-width layout */}
      <main className="w-full px-6 sm:px-10 lg:px-14 py-8">

        <Link to="/" className="inline-flex items-center gap-1 text-sm text-[#069494] hover:underline mb-6 font-medium">
          ← Back to Home
        </Link>

        {/* Profile header */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5">
            <div className="w-20 h-20 rounded-full bg-[#069494] flex items-center justify-center text-white text-2xl font-bold shrink-0">
              {initials}
            </div>
            <div className="flex-1 text-center sm:text-left">
              <h1 className="font-playfair text-3xl font-semibold text-[#264653]">{user.username}</h1>
              <p className="text-gray-500 text-sm mt-1">{user.email}</p>
              <p className="text-gray-400 text-xs mt-1">Member since {user.member_since}</p>
            </div>
            <button
              onClick={handleInvite}
              className={`shrink-0 px-5 py-2 rounded-full font-semibold text-sm transition ${
                inviteSent ? 'bg-emerald-500 text-white' : 'bg-[#069494] hover:bg-[#057878] text-white'
              }`}
            >
              {inviteSent ? '✓ Invite Sent!' : '👥 Invite Friends'}
            </button>
          </div>

          {/* Stats */}
          <div className="flex justify-center sm:justify-start gap-10 mt-5 pt-5 border-t border-[#F1FAEE]">
            {[
              { value: user.review_count,              label: 'Reviews'      },
              { value: user.liked_restaurants.length,  label: 'Liked Places' },
              { value: 'CA',                           label: 'Region'       },
            ].map(({ value, label }) => (
              <div key={label} className="text-center">
                <p className="text-2xl font-bold text-[#069494]">{value}</p>
                <p className="text-xs text-gray-400 mt-0.5">{label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Liked restaurants */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <h2 className="font-playfair text-xl font-semibold text-[#264653] mb-4">❤️ Places I Loved</h2>
          {user.liked_restaurants.length === 0 ? (
            <p className="text-gray-400 text-sm">No liked places yet. Start exploring!</p>
          ) : (
            <div className="flex gap-4 overflow-x-auto no-scrollbar pb-2">
              {user.liked_restaurants.map((r) => (
                <RestaurantCard key={r.gmap_id} restaurant={r} />
              ))}
            </div>
          )}
        </div>

        {/* Two-column layout for Preferences + Account */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">

          {/* Preferences */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h2 className="font-playfair text-xl font-semibold text-[#264653] mb-1">⚙️ My Preferences</h2>
            <p className="text-sm text-gray-400 mb-4">We'll use these to personalize your recommendations</p>
            <div className="grid grid-cols-2 gap-3">
              {(Object.keys(preferences) as PreferenceKey[]).map((key) => {
                const { label, emoji } = PREFERENCE_LABELS[key];
                const active = preferences[key];
                return (
                  <button
                    key={key}
                    onClick={() => togglePref(key)}
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm font-medium transition-all ${
                      active
                        ? 'bg-[#FFC0CB]/20 border-[#FFC0CB] text-[#264653]'
                        : 'bg-[#F1FAEE] border-gray-200 text-gray-500 hover:border-[#069494]/40'
                    }`}
                  >
                    <span>{emoji}</span>
                    {label}
                    {active && <span className="ml-auto text-[#069494]">✓</span>}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Account settings — no Payment Methods */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h2 className="font-playfair text-xl font-semibold text-[#264653] mb-4">👤 Account</h2>
            <div className="space-y-3">
              {[
                { icon: '✏️', label: 'Edit Profile',  sub: 'Update your name and email' },
                { icon: '🔔', label: 'Notifications', sub: 'Manage alerts and digests' },
                { icon: '🔒', label: 'Privacy',       sub: 'Control your data and visibility' },
                { icon: '🚪', label: 'Sign Out',      sub: 'Log out of your account' },
              ].map(({ icon, label, sub }) => (
                <button
                  key={label}
                  className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-[#F1FAEE] transition text-left group"
                >
                  <span className="text-xl w-8 text-center">{icon}</span>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-[#264653] group-hover:text-[#069494] transition">{label}</p>
                    <p className="text-xs text-gray-400">{sub}</p>
                  </div>
                  <span className="text-gray-300 group-hover:text-[#069494] transition">›</span>
                </button>
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
