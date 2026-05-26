import { useRef } from 'react';
import type { Restaurant } from '../types';
import RestaurantCard from './RestaurantCard';

interface RestaurantRowProps {
  title: string;
  emoji: string;
  restaurants: Restaurant[];
  isLast?: boolean;
}

export default function RestaurantRow({ title, emoji, restaurants, isLast }: RestaurantRowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  function scroll(direction: 'left' | 'right') {
    if (!scrollRef.current) return;
    scrollRef.current.scrollBy({ left: direction === 'right' ? 780 : -780, behavior: 'smooth' });
  }

  if (restaurants.length === 0) return null;

  return (
    <section className="pt-12 pb-4">
      {/* Row header */}
      <div className="flex items-center justify-between mb-6 px-1">
        <h2 className="font-playfair text-2xl font-semibold text-[#264653] flex items-center gap-2">
          <span>{emoji}</span>
          {title}
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => scroll('left')}
            aria-label="Scroll left"
            className="w-9 h-9 flex items-center justify-center rounded-full bg-white border border-[#069494]/30 shadow-sm hover:bg-[#069494] hover:text-white text-[#069494] transition-all text-xl font-bold"
          >
            ‹
          </button>
          <button
            onClick={() => scroll('right')}
            aria-label="Scroll right"
            className="w-9 h-9 flex items-center justify-center rounded-full bg-white border border-[#069494]/30 shadow-sm hover:bg-[#069494] hover:text-white text-[#069494] transition-all text-xl font-bold"
          >
            ›
          </button>
        </div>
      </div>

      {/* Scrollable cards */}
      <div ref={scrollRef} className="flex gap-5 overflow-x-auto no-scrollbar pb-4">
        {restaurants.map((restaurant) => (
          <RestaurantCard key={restaurant.gmap_id} restaurant={restaurant} />
        ))}
      </div>

      {/* Grey separator line with breathing room */}
      {!isLast && <div className="mt-12 border-b border-gray-200/70" />}
    </section>
  );
}
