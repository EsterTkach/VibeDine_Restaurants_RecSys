import { useRef } from 'react';
import RestaurantCard from './RestaurantCard';

interface RestaurantRowProps {
  title: string;
  emoji?: string;
  restaurants: any[]; 
}

export default function RestaurantRow({ title, emoji, restaurants }: RestaurantRowProps) {
  const sliderRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: 'left' | 'right') => {
    if (sliderRef.current) {
      const scrollAmount = 300;
      sliderRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div 
      className="restaurant-row-container" 
      style={{ 
        width: '100%', 
        display: 'block', 
        margin: 0,
        position: 'relative'
      }}
    >
      {/* 🌟 REWORKED STYLE BLOCK: Handles the smooth hover fade effect */}
      <style>{`
        .restaurant-slider::-webkit-scrollbar { 
          display: none !important; 
        }

        /* Start the arrow hidden and slightly transparent */
        .nav-arrow-btn {
          opacity: 0;
          transition: opacity 0.25s ease-in-out, transform 0.2s ease;
        }

        /* When the parent row container is hovered, fade the arrows in */
        .restaurant-row-container:hover .nav-arrow-btn {
          opacity: 1;
        }

        /* Subtle interactive bounce when hovering directly over the arrow button itself */
        .nav-arrow-btn:hover {
          background-color: #ffffff !important;
          transform: translateY(-50%) scale(1.1) !important;
        }

        @media (max-width: 768px) {
          .nav-arrow-btn {
            display: none !important;
          }
        }
      `}</style>
      
      {/* Row Header */}
      <div 
        className="row-header" 
        style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px', 
          marginBottom: '12px', 
          paddingLeft: '16px', 
          paddingRight: '16px' 
        }}
      >
        {emoji && <span style={{ fontSize: '1.25rem' }} role="img" aria-label={title}>{emoji}</span>}
        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#3d2817', margin: 0 }}>
          {title}
        </h2>
      </div>

      {/* Floating Left Arrow */}
      <button
        className="nav-arrow-btn"
        onClick={() => scroll('left')}
        style={{
          position: 'absolute',
          left: '12px',
          top: '50%',
          transform: 'translateY(-50%)',
          zIndex: 10,
          width: '38px',
          height: '38px',
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid rgba(0,0,0,0.08)',
          boxShadow: '0 4px 14px rgba(0,0,0,0.08)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '32px',
          lineHeight: '1',
          color: '#3d2817'
        }}
      >
        ‹
      </button>

      {/* Floating Right Arrow */}
      <button
        className="nav-arrow-btn"
        onClick={() => scroll('right')}
        style={{
          position: 'absolute',
          right: '12px',
          top: '50%',
          transform: 'translateY(-50%)',
          zIndex: 10,
          width: '38px',
          height: '38px',
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid rgba(0,0,0,0.08)',
          boxShadow: '0 4px 14px rgba(0,0,0,0.08)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '32px',
          lineHeight: '1',
          color: '#3d2817'
        }}
      >
        ›
      </button>
      
      {/* Horizontal Slider Wrapper */}
      <div 
        className="restaurant-slider"
        ref={sliderRef}
        style={{
          display: 'flex',
          flexWrap: 'nowrap',      
          overflowX: 'auto',       
          overflowY: 'hidden',     
          gap: '16px',
          paddingLeft: '16px',
          paddingRight: '16px',
          paddingBottom: '16px',   
          width: '100%',
          boxSizing: 'border-box',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none',
          msOverflowStyle: 'none'
        }}
      >
        {restaurants.map((restaurant) => (
          <div 
            key={restaurant.id} 
            className="slider-item" 
            style={{ flex: '0 0 256px', width: '256px', minWidth: '256px' }}
          >
            <RestaurantCard restaurant={restaurant} />
          </div>
        ))}
      </div>
    </div>
  );
}