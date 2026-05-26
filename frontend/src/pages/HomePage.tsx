import { useState, useMemo } from 'react';
import Navbar from '../components/Navbar';
import RestaurantRow from '../components/RestaurantRow';
import { MOCK_ROWS } from '../data/mockData';

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredRows = useMemo(() => {
    if (!searchQuery.trim()) return MOCK_ROWS;
    const q = searchQuery.toLowerCase();
    return MOCK_ROWS.map((row) => ({
      ...row,
      restaurants: row.restaurants.filter(
        (r) => r.name.toLowerCase().includes(q) || r.category.toLowerCase().includes(q)
      ),
    })).filter((row) => row.restaurants.length > 0);
  }, [searchQuery]);

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar onSearch={setSearchQuery} />

      {/* Hero banner */}
      <div className="bg-gradient-to-r from-[#264653] to-[#069494] text-white py-10 px-6 flex justify-center">
        <h1 className="font-title text-3xl sm:text-4xl leading-tight text-center">
          Find your next favorite restaurant
        </h1>
      </div>

      {/* Main content — full width */}
      <main className="w-full px-6 sm:px-10 lg:px-14 pt-4 pb-12">

        {searchQuery && (
          <div className="mb-4 mt-4 flex items-center gap-2">
            <span className="text-sm text-[#264653]/70">
              Results for <strong>"{searchQuery}"</strong>
            </span>
            <button onClick={() => setSearchQuery('')} className="text-sm text-[#069494] hover:underline font-medium">
              Clear
            </button>
          </div>
        )}

        {filteredRows.length === 0 ? (
          <div className="text-center py-20 text-[#264653]/40">
            <p className="text-5xl mb-4">🔍</p>
            <p className="text-lg font-playfair font-semibold">No restaurants found for "{searchQuery}"</p>
            <p className="text-sm mt-1">Try a different cuisine or restaurant name</p>
          </div>
        ) : (
          filteredRows.map((row, index) => (
            <RestaurantRow
              key={row.id}
              title={row.title}
              emoji={row.emoji}
              restaurants={row.restaurants}
              isLast={index === filteredRows.length - 1}
            />
          ))
        )}
      </main>
    </div>
  );
}
