import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

interface NavbarProps {
  onSearch?: (query: string) => void;
}

function SearchIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8" />
      <path strokeLinecap="round" d="m21 21-4.35-4.35" />
    </svg>
  );
}

export default function Navbar({ onSearch }: NavbarProps) {
  const [query, setQuery] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

  const isHome    = location.pathname === '/';
  const isProfile = location.pathname === '/profile';

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setQuery(e.target.value);
    onSearch?.(e.target.value);
  }

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-200">
      <div className="w-full px-6 lg:px-16 h-20 flex items-center justify-between gap-6">

        {/* Logo — Parisienne only here */}
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <span className="text-3xl">🍽️</span>
          <span className="font-title text-3xl text-[#3d2817] leading-none">VibeDine</span>
        </Link>

        {/* Search bar — icon on the RIGHT */}
        <form onSubmit={(e) => e.preventDefault()} className="flex-1 max-w-2xl">
          <div className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={handleChange}
              placeholder="Search restaurants, cuisines..."
              className="w-full pl-5 pr-12 py-3 rounded-full border-2 border-transparent bg-white/15 text-white placeholder-white/60 text-sm focus:outline-none focus:bg-white focus:text-[#3d2817] focus:placeholder-gray-400 focus:border-[#a0826d] transition-all"
            />
            <span className="absolute right-4 text-[#a0826d] pointer-events-none flex items-center">
              <SearchIcon />
            </span>
          </div>
        </form>

        {/* Nav links — hide the link for the current page */}
        <div className="flex items-center gap-4 shrink-0">
          {!isHome && (
            <button
              onClick={() => navigate('/')}
              className="hidden sm:block text-sm text-white/80 hover:text-white font-medium transition"
            >
              Home
            </button>
          )}
          {!isProfile && (
            <Link
              to="/profile"
              className="flex items-center gap-2 bg-[#3d2817] hover:bg-[#8b6f47] text-white text-sm font-semibold px-5 py-2.5 rounded-full transition shadow-md"
            >
              <span>👤</span>
              <span className="hidden sm:block">My Profile</span>
            </Link>
          )}
        </div>

      </div>
    </nav>
  );
}
