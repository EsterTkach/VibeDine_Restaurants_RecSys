import RestaurantCard from './RestaurantCard';

interface RestaurantRowProps {
  title: string;
  emoji?: string;
  restaurants: any[]; 
}

export default function RestaurantRow({ title, emoji, restaurants }: RestaurantRowProps) {
  return (
    <div 
      className="restaurant-row-container"
      style={{
        width: '100%',
        display: 'block',
        margin: 0 // Margins are zeroed out because the parent's layout 'gap' handles it perfectly now
      }}
    >
      
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
      
      {/* Horizontal Slider Wrapper */}
      <div 
        className="restaurant-slider"
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
          WebkitOverflowScrolling: 'touch' 
        }}
      >
        {restaurants.map((restaurant) => (
          <div 
            key={restaurant.id} 
            className="slider-item"
            style={{
              flex: '0 0 256px',    
              width: '256px',
              minWidth: '256px'
            }}
          >
            <RestaurantCard restaurant={restaurant} />
          </div>
        ))}
      </div>

    </div>
  );
}