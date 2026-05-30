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
    <div className="min-h-screen bg-[#eadfcf]">
      <Navbar />

      {/* Full-width layout */}
      <main className="w-full px-6 sm:px-10 lg:px-14 py-12">

        <Link to="/" className="inline-flex items-center gap-1 text-sm text-[#592d25] hover:underline mb-8 font-medium">
          ← Back to Home
        </Link>

        {/* Profile header */}
        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
          <div className="flex flex-col sm:flex-row items-center sm:items-start gap-8">
            <div className="w-24 h-24 rounded-full bg-[#c9a67c] flex items-center justify-center text-white text-2xl font-bold shrink-0">
              {initials}
            </div>
            <div className="flex-1 text-center sm:text-left">
              <h1 className="font-modern text-3xl font-semibold text-[#264653]">{user.username}</h1>
              <p className="text-gray-500 text-sm mt-2">{user.email}</p>
              <p className="text-gray-400 text-xs mt-2">Member since {user.member_since}</p>
            </div>
            <button
              onClick={handleInvite}
              className={`shrink-0 px-6 py-3 rounded-full font-semibold text-sm transition ${
                inviteSent ? 'bg-emerald-500 text-white' : 'bg-[#c9a67c] hover:bg-[#b5945a] text-white'
              }`}
            >
              {inviteSent ? '✓ Invite Sent!' : '👥 Invite Friends'}
            </button>
          </div>

          {/* Stats */}
          <div className="flex justify-center sm:justify-start gap-16 mt-8 pt-8 border-t border-[#eadfcf]">
            {[
              { value: user.review_count,              label: 'Reviews'      },
              { value: user.liked_restaurants.length,  label: 'Liked Places' },
              { value: 'CA',                           label: 'Region'       },
            ].map(({ value, label }) => (
              <div key={label} className="text-center">
                <p className="text-3xl font-bold text-[#c9a67c]">{value}</p>
                <p className="text-xs text-gray-400 mt-1">{label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Liked restaurants */}
        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
          <h2 className="font-modern text-xl font-semibold text-[#264653] mb-6">❤️ Places I Loved</h2>
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

          {/* Preferences */}
          <div className="bg-white rounded-2xl shadow-sm p-8">
            <h2 className="font-modern text-xl font-semibold text-[#264653] mb-2">⚙️ My Preferences</h2>
            <p className="text-sm text-gray-400 mb-6">We'll use these to personalize your recommendations</p>
            <div className="grid grid-cols-2 gap-4">
              {(Object.keys(preferences) as PreferenceKey[]).map((key) => {
                const { label, emoji } = PREFERENCE_LABELS[key];
                const active = preferences[key];
                return (
                  <button
                    key={key}
                    onClick={() => togglePref(key)}
                    className={`flex items-center gap-2 px-4 py-3 rounded-xl border text-sm font-medium transition-all ${
                      active
                        ? 'bg-[#c9a67c]/20 border-[#c9a67c] text-[#264653]'
                        : 'bg-[#eadfcf] border-gray-200 text-gray-500 hover:border-[#c9a67c]/40'
                    }`}
                  >
                    <span>{emoji}</span>
                    {label}
                    {active && <span className="ml-auto text-[#c9a67c]">✓</span>}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Account settings — no Payment Methods */}
          <div className="bg-white rounded-2xl shadow-sm p-8">
            <h2 className="font-modern text-xl font-semibold text-[#264653] mb-6">👤 Account</h2>
            <div className="space-y-4">
              {[
                { icon: '✏️', label: 'Edit Profile',  sub: 'Update your name and email' },
                { icon: '🔔', label: 'Notifications', sub: 'Manage alerts and digests' },
                { icon: '🔒', label: 'Privacy',       sub: 'Control your data and visibility' },
                { icon: '🚪', label: 'Sign Out',      sub: 'Log out of your account' },
              ].map(({ icon, label, sub }) => (
                <button
                  key={label}
                  className="w-full flex items-center gap-3 p-4 rounded-xl hover:bg-[#eadfcf] transition text-left group"
                >
                  <span className="text-xl w-8 text-center">{icon}</span>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-[#264653] group-hover:text-[#c9a67c] transition">{label}</p>
                    <p className="text-xs text-gray-400">{sub}</p>
                  </div>
                  <span className="text-gray-300 group-hover:text-[#c9a67c] transition">›</span>
                </button>
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
