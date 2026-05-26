import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { MOCK_ROWS } from '../data/mockData';
import type { Restaurant } from '../types';

interface Review {
  id: string;
  author: string;
  avatar: string;
  date: string;
  rating: number;
  text: string;
}

type SortOption = 'newest' | 'oldest' | 'highest' | 'lowest';

const MOCK_REVIEWS: Review[] = [
  { id: 'r1',  author: 'Sarah M.',  avatar: 'SM', date: '2025-03-15', rating: 5, text: "Absolutely incredible experience! The food was perfectly cooked and the service was impeccable. One of the best meals I've had in LA. Will definitely be back soon." },
  { id: 'r2',  author: 'James K.',  avatar: 'JK', date: '2025-02-28', rating: 4, text: 'Great atmosphere and really solid food. The wait time was a bit long but totally worth it. The ambiance is lovely, especially in the evening.' },
  { id: 'r3',  author: 'Emily R.',  avatar: 'ER', date: '2025-01-12', rating: 5, text: "One of the best dining experiences I've had in years. The menu is creative and the wine selection is excellent. Highly recommend for a special occasion." },
  { id: 'r4',  author: 'Daniel T.', avatar: 'DT', date: '2024-12-03', rating: 3, text: 'Decent place but a bit overpriced for what you get. The appetizers were fantastic but the main courses were just average. Mixed feelings overall.' },
  { id: 'r5',  author: 'Lisa P.',   avatar: 'LP', date: '2024-11-22', rating: 4, text: 'Lovely restaurant with a beautiful interior. The pasta dishes were exceptional — really recommend the linguine. Staff was friendly and attentive.' },
  { id: 'r6',  author: 'Mark W.',   avatar: 'MW', date: '2024-10-10', rating: 5, text: 'Perfect spot for a special occasion. Staff were attentive without being intrusive. Outstanding food quality from start to finish — desserts especially.' },
  { id: 'r7',  author: 'Anna B.',   avatar: 'AB', date: '2024-09-15', rating: 2, text: 'Disappointed with my visit. Food arrived lukewarm and service was slow despite a half-empty restaurant. Expected much more based on other reviews.' },
  { id: 'r8',  author: 'Tom H.',    avatar: 'TH', date: '2024-08-08', rating: 4, text: 'Solid place for dinner. Not the most adventurous menu but everything is executed really well. The bread basket alone is worth the visit.' },
  { id: 'r9',  author: 'Rachel G.', avatar: 'RG', date: '2024-07-20', rating: 5, text: 'Came here for a birthday dinner and it was magical. Chef came out personally to greet our table. Incredible flavors throughout the tasting menu.' },
  { id: 'r10', author: 'Chris N.',  avatar: 'CN', date: '2024-06-05', rating: 3, text: "It's fine — nothing extraordinary. The location is great and the interior is pretty but the food doesn't justify the price point for everyday dining." },
];

function findById(id: string): Restaurant | undefined {
  for (const row of MOCK_ROWS) {
    const found = row.restaurants.find((r) => r.gmap_id === id);
    if (found) return found;
  }
  return undefined;
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function Stars({ rating, size = 'md' }: { rating: number; size?: 'sm' | 'md' | 'lg' }) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  const cls = size === 'lg' ? 'text-xl' : size === 'sm' ? 'text-xs' : 'text-sm';
  return (
    <span className="flex items-center gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className={`${cls} ${i < full ? 'text-[#FCE883]' : half && i === full ? 'text-[#FCE883]/60' : 'text-gray-300'}`}>★</span>
      ))}
    </span>
  );
}

function ReviewCard({ review }: { review: Review }) {
  return (
    <div className="bg-[#F1FAEE] rounded-2xl p-4">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-9 h-9 rounded-full bg-[#069494] flex items-center justify-center text-white text-xs font-bold shrink-0">
          {review.avatar}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-[#264653]">{review.author}</p>
          <p className="text-xs text-gray-400">{formatDate(review.date)}</p>
        </div>
        <Stars rating={review.rating} size="sm" />
      </div>
      <p className="text-sm text-gray-600 leading-relaxed">{review.text}</p>
    </div>
  );
}

export default function RestaurantDetailPage() {
  const { id } = useParams<{ id: string }>();
  const restaurant = id ? findById(id) : undefined;

  const [sortBy, setSortBy]         = useState<SortOption>('newest');
  const [filterStars, setFilterStars] = useState<number>(0);
  const [saved, setSaved]           = useState(false);

  const sortedReviews = [...MOCK_REVIEWS]
    .filter((r) => filterStars === 0 || r.rating === filterStars)
    .sort((a, b) => {
      if (sortBy === 'newest')  return new Date(b.date).getTime() - new Date(a.date).getTime();
      if (sortBy === 'oldest')  return new Date(a.date).getTime() - new Date(b.date).getTime();
      if (sortBy === 'highest') return b.rating - a.rating;
      return a.rating - b.rating;
    });

  if (!restaurant) {
    return (
      <div className="min-h-screen bg-[#F1FAEE]">
        <Navbar />
        <div className="flex flex-col items-center justify-center py-40 text-[#264653]/40">
          <p className="text-6xl mb-4">🍽️</p>
          <p className="font-playfair text-xl font-semibold">Restaurant not found</p>
          <Link to="/" className="mt-4 text-[#069494] hover:underline text-sm">← Back to Home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />

      {/* ── Full-width hero ─────────────────────────────────────────────── */}
      <div className="relative w-full h-80 sm:h-96 overflow-hidden">
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="w-full h-full object-cover"
        />
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#264653]/90 via-[#264653]/30 to-transparent" />

        {/* Back link */}
        <Link
          to="/"
          className="absolute top-4 left-6 text-white/90 hover:text-white text-sm font-medium flex items-center gap-1 bg-black/20 backdrop-blur-sm px-3 py-1.5 rounded-full transition"
        >
          ← Back
        </Link>

        {/* Name + badges overlaid at bottom of hero */}
        <div className="absolute bottom-0 left-0 right-0 px-6 sm:px-10 lg:px-14 pb-6">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <span className="inline-block bg-[#FCE883] text-[#264653] text-xs font-bold px-3 py-0.5 rounded-full mb-2">
                {restaurant.category}
              </span>
              <h1 className="font-playfair text-3xl sm:text-4xl font-semibold text-white leading-tight drop-shadow">
                {restaurant.name}
              </h1>
            </div>
            <div className="flex gap-2 items-center shrink-0">
              {restaurant.is_open !== undefined && (
                <span className={`text-xs font-semibold px-3 py-1 rounded-full ${restaurant.is_open ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-600'}`}>
                  {restaurant.is_open ? '● Open Now' : '● Closed'}
                </span>
              )}
              {restaurant.price_level && (
                <span className="text-xs font-bold px-3 py-1 rounded-full bg-white/20 text-white backdrop-blur-sm border border-white/30">
                  {restaurant.price_level}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ── Info strip ──────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-gray-100 shadow-sm">
        <div className="w-full px-6 sm:px-10 lg:px-14 py-3 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-[#264653]">
          <span className="flex items-center gap-1.5 font-semibold">
            <Stars rating={restaurant.avg_rating} size="sm" />
            {restaurant.avg_rating.toFixed(1)}
            <span className="text-gray-400 font-normal">({restaurant.review_count.toLocaleString()})</span>
          </span>
          {restaurant.address && (
            <>
              <span className="text-gray-200">|</span>
              <span className="text-gray-500">📍 {restaurant.address}</span>
            </>
          )}
          {restaurant.service_options?.length && (
            <>
              <span className="text-gray-200">|</span>
              <span className="text-gray-500">🛎️ {restaurant.service_options.join(' · ')}</span>
            </>
          )}
        </div>
      </div>

      {/* ── Two-column body ─────────────────────────────────────────────── */}
      <div className="w-full px-6 sm:px-10 lg:px-14 py-8">
        <div className="flex flex-col lg:flex-row gap-8">

          {/* LEFT — details + CTAs (40%) */}
          <div className="lg:w-[38%] shrink-0 space-y-4">

            {/* CTA buttons */}
            <div className="flex gap-3">
              <button
                onClick={() => setSaved((s) => !s)}
                className={`flex-1 font-semibold py-3 rounded-2xl transition text-sm ${
                  saved
                    ? 'bg-[#FFC0CB] text-[#264653]'
                    : 'bg-[#069494] hover:bg-[#057878] text-white'
                }`}
              >
                {saved ? '❤️ Saved!' : '♡ Save to Favorites'}
              </button>
              <button className="flex-1 bg-white hover:bg-[#F1FAEE] text-[#264653] font-semibold py-3 rounded-2xl border border-[#069494]/30 transition text-sm">
                Share 🔗
              </button>
            </div>

            {/* Details card */}
            <div className="bg-white rounded-2xl shadow-sm p-5 space-y-3">
              <h2 className="font-playfair text-lg font-semibold text-[#264653]">About</h2>

              {restaurant.address && (
                <div className="flex items-start gap-3 p-3 rounded-xl bg-[#F1FAEE]">
                  <span className="text-lg shrink-0">📍</span>
                  <div>
                    <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">Address</p>
                    <p className="text-sm text-[#264653] font-medium mt-0.5">{restaurant.address}</p>
                  </div>
                </div>
              )}

              <div className="flex items-start gap-3 p-3 rounded-xl bg-[#F1FAEE]">
                <span className="text-lg shrink-0">⭐</span>
                <div>
                  <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">Rating</p>
                  <p className="text-sm text-[#264653] font-medium mt-0.5">
                    {restaurant.avg_rating.toFixed(1)} / 5 &nbsp;·&nbsp; {restaurant.review_count.toLocaleString()} reviews
                  </p>
                </div>
              </div>

              {restaurant.price_level && (
                <div className="flex items-start gap-3 p-3 rounded-xl bg-[#F1FAEE]">
                  <span className="text-lg shrink-0">💰</span>
                  <div>
                    <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">Price Range</p>
                    <p className="text-sm text-[#264653] font-medium mt-0.5">{restaurant.price_level}</p>
                  </div>
                </div>
              )}

              {restaurant.service_options?.length && (
                <div className="flex items-start gap-3 p-3 rounded-xl bg-[#F1FAEE]">
                  <span className="text-lg shrink-0">🛎️</span>
                  <div>
                    <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">Service Options</p>
                    <p className="text-sm text-[#264653] font-medium mt-0.5">{restaurant.service_options.join(' · ')}</p>
                  </div>
                </div>
              )}

              {restaurant.dining_options?.length && (
                <div className="flex items-start gap-3 p-3 rounded-xl bg-[#F1FAEE]">
                  <span className="text-lg shrink-0">🍴</span>
                  <div>
                    <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">Dining Options</p>
                    <p className="text-sm text-[#264653] font-medium mt-0.5">{restaurant.dining_options.join(' · ')}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* RIGHT — reviews (60%) */}
          <div className="flex-1 min-w-0">
            <div className="bg-white rounded-2xl shadow-sm p-5">

              {/* Header + sort */}
              <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                <h2 className="font-playfair text-lg font-semibold text-[#264653]">
                  Reviews <span className="text-gray-400 font-normal text-base">({MOCK_REVIEWS.length})</span>
                </h2>
                <div className="flex items-center gap-2">
                  <label className="text-xs text-gray-400 font-medium whitespace-nowrap">Sort:</label>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as SortOption)}
                    className="text-sm border border-gray-200 rounded-full px-3 py-1.5 text-[#264653] bg-white focus:outline-none focus:border-[#069494] transition"
                  >
                    <option value="newest">Newest</option>
                    <option value="oldest">Oldest</option>
                    <option value="highest">Highest Rated</option>
                    <option value="lowest">Lowest Rated</option>
                  </select>
                </div>
              </div>

              {/* Star filter pills */}
              <div className="flex items-center gap-1.5 flex-wrap mb-5">
                <span className="text-xs text-gray-400 font-medium mr-1">Filter:</span>
                {[0, 5, 4, 3, 2, 1].map((star) => (
                  <button
                    key={star}
                    onClick={() => setFilterStars(star)}
                    className={`text-xs px-3 py-1 rounded-full border transition font-medium ${
                      filterStars === star
                        ? 'bg-[#FCE883] border-[#FCE883] text-[#264653]'
                        : 'bg-white border-gray-200 text-gray-500 hover:border-[#069494]/40'
                    }`}
                  >
                    {star === 0 ? 'All' : `${star}★`}
                  </button>
                ))}
              </div>

              {/* Review list */}
              {sortedReviews.length === 0 ? (
                <p className="text-gray-400 text-sm text-center py-10">No reviews match your filter.</p>
              ) : (
                <div className="space-y-3">
                  {sortedReviews.map((review) => (
                    <ReviewCard key={review.id} review={review} />
                  ))}
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
