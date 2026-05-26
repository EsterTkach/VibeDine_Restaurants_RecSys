import { Link } from 'react-router-dom';
import type { Restaurant } from '../types';

interface RestaurantCardProps {
  restaurant: Restaurant;
}

function StarRating({ rating }: { rating: number }) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  return (
    <span className="flex items-center justify-center gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className={`text-sm ${i < full ? 'text-[#FCE883]' : half && i === full ? 'text-[#FCE883]/60' : 'text-gray-300'}`}>
          ★
        </span>
      ))}
    </span>
  );
}

export default function RestaurantCard({ restaurant }: RestaurantCardProps) {
  return (
    <Link
      to={`/restaurant/${restaurant.gmap_id}`}
      className="flex-shrink-0 w-[280px] bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-xl hover:-translate-y-1.5 transition-all duration-200 group"
    >
      {/* Image */}
      <div className="relative h-44 overflow-hidden">
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        {restaurant.is_open !== undefined && (
          <span className={`absolute top-2.5 right-2.5 text-xs font-semibold px-2.5 py-0.5 rounded-full shadow-sm ${restaurant.is_open ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-600'}`}>
            {restaurant.is_open ? 'Open' : 'Closed'}
          </span>
        )}
        {restaurant.price_level && (
          <span className="absolute bottom-2.5 left-2.5 text-xs font-bold text-white bg-[#264653]/75 px-2.5 py-0.5 rounded-full backdrop-blur-sm">
            {restaurant.price_level}
          </span>
        )}
      </div>

      {/* Info — all centered */}
      <div className="p-4 flex flex-col items-center text-center gap-1.5">
        <h3 className="font-semibold text-[#264653] text-base leading-snug" title={restaurant.name}>
          {restaurant.name}
        </h3>
        <span className="text-xs text-[#264653] bg-[#FCE883] px-2.5 py-0.5 rounded-full font-medium">
          {restaurant.category}
        </span>
        <div className="flex items-center justify-center gap-1.5 mt-0.5">
          <StarRating rating={restaurant.avg_rating} />
          <span className="text-xs font-bold text-[#264653]">{restaurant.avg_rating.toFixed(1)}</span>
          <span className="text-xs text-gray-400">({restaurant.review_count.toLocaleString()})</span>
        </div>
      </div>
    </Link>
  );
}
