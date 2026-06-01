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
    <section className="pt-16 pb-8">
      {/* Row header */}
      <div className="flex items-center justify-between mb-10 px-1">
        <h2 className="font-modern text-3xl lg:text-4xl font-semibold text-[#3d2817] flex items-center gap-3">
          <span className="text-3xl">{emoji}</span>
          {title}
        </h2>
        <div className="flex gap-3">
          <button
            onClick={() => scroll('left')}
            aria-label="Scroll left"
            className="w-12 h-12 flex items-center justify-center rounded-full bg-white border-2 border-[#a0826d]/40 shadow-lg hover:bg-[#a0826d] hover:text-white text-[#a0826d] hover:border-[#a0826d] transition-all text-2xl font-bold"
          >
            ‹
          </button>
          <button
            onClick={() => scroll('right')}
            aria-label="Scroll right"
            className="w-12 h-12 flex items-center justify-center rounded-full bg-white border-2 border-[#a0826d]/40 shadow-lg hover:bg-[#a0826d] hover:text-white text-[#a0826d] hover:border-[#a0826d] transition-all text-2xl font-bold"
          >
            ›
          </button>
        </div>
      </div>

      {/* Scrollable cards */}
      <div ref={scrollRef} className="flex gap-8 overflow-x-auto no-scrollbar pb-8">
        {restaurants.map((restaurant) => (
          <RestaurantCard key={restaurant.gmap_id} restaurant={restaurant} />
        ))}
      </div>

      {/* Separator line */}
      {!isLast && <div className="mt-16 border-b border-gray-200/60" />}
    </section>
  );
}
