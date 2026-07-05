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
      <style>{`
        .restaurant-slider::-webkit-scrollbar { 
          display: none !important; 
        }

        .nav-arrow-btn {
          opacity: 0;
          transition: opacity 0.25s ease-in-out, transform 0.2s ease;
        }

        .restaurant-row-container:hover .nav-arrow-btn {
          opacity: 1;
        }

        .nav-arrow-btn:hover {
          background-color: #ffffff !important;
          transform: translateY(-50%) scale(1.1) !important;
        }

        .slider-wrapper {
          position: relative;
        }

        .slider-wrapper::before,
        .slider-wrapper::after {
          content: '';
          position: absolute;
          top: 0;
          bottom: 0;
          width: 40px;
          z-index: 5;
          pointer-events: none;
          transition: opacity 0.3s ease;
        }

        .slider-wrapper::before {
          left: 0;
          background: linear-gradient(to right, rgba(255,255,255,0.9), transparent);
        }

        .slider-wrapper::after {
          right: 0;
          background: linear-gradient(to left, rgba(255,255,255,0.9), transparent);
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
          gap: '6px', 
          marginBottom: '12px', 
          paddingLeft: '20px', 
          paddingRight: '20px' 
        }}
      >
        {emoji && <span style={{ fontSize: '1rem' }} role="img" aria-label={title}>{emoji}</span>}
        <h2 style={{ fontSize: '1rem', fontWeight: '700', color: '#2d1f10', margin: 0, letterSpacing: '-0.01em' }}>
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
          top: '55%',
          transform: 'translateY(-50%)',
          zIndex: 10,
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.97)',
          border: '1px solid rgba(0,0,0,0.06)',
          boxShadow: '0 4px 16px rgba(0,0,0,0.1)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '28px',
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
          top: '55%',
          transform: 'translateY(-50%)',
          zIndex: 10,
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.97)',
          border: '1px solid rgba(0,0,0,0.06)',
          boxShadow: '0 4px 16px rgba(0,0,0,0.1)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '28px',
          lineHeight: '1',
          color: '#3d2817'
        }}
      >
        ›
      </button>
      
      {/* Horizontal Slider Wrapper with fade edges */}
      <div className="slider-wrapper">
        <div 
          className="restaurant-slider"
          ref={sliderRef}
          style={{
            display: 'flex',
            flexWrap: 'nowrap',      
            overflowX: 'auto',       
            overflowY: 'hidden',     
            gap: '14px',
            paddingLeft: '20px',
            paddingRight: '20px',
            paddingBottom: '12px',
            paddingTop: '4px',
            width: '100%',
            boxSizing: 'border-box',
            WebkitOverflowScrolling: 'touch',
            scrollbarWidth: 'none',
            msOverflowStyle: 'none'
          }}
        >
          {restaurants.map((restaurant) => (
            <div 
              key={restaurant.id || restaurant.gmap_id} 
              className="slider-item" 
              style={{ flex: '0 0 200px', width: '200px', minWidth: '200px' }}
            >
              <RestaurantCard restaurant={restaurant} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}