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
    <nav className="sticky top-0 z-50 bg-[#264653] shadow-md">
      <div className="w-full px-6 h-16 flex items-center justify-between gap-4">

        {/* Logo — Parisienne only here */}
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <span className="text-2xl">🍽️</span>
          <span className="font-title text-3xl text-white leading-none">VibeDine</span>
        </Link>

        {/* Search bar — icon on the RIGHT */}
        <form onSubmit={(e) => e.preventDefault()} className="flex-1 max-w-xl">
          <div className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={handleChange}
              placeholder="Search restaurants, cuisines..."
              className="w-full pl-4 pr-10 py-2 rounded-full border-2 border-transparent bg-white/10 text-white placeholder-white/50 text-sm focus:outline-none focus:bg-white focus:text-[#264653] focus:placeholder-gray-400 focus:border-[#069494] transition-all"
            />
            <span className="absolute right-3 text-[#069494] pointer-events-none flex items-center">
              <SearchIcon />
            </span>
          </div>
        </form>

        {/* Nav links — hide the link for the current page */}
        <div className="flex items-center gap-3 shrink-0">
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
              className="flex items-center gap-2 bg-[#069494] hover:bg-[#057878] text-white text-sm font-semibold px-4 py-2 rounded-full transition"
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
