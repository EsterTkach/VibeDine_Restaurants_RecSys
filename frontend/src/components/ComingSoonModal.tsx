import "./ComingSoonModal.css";

interface ComingSoonModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ComingSoonModal({
  isOpen,
  onClose,
}: ComingSoonModalProps) {
  if (!isOpen) return null;

  return (
    <div className="coming-soon-overlay" onClick={onClose}>
      <div
        className="coming-soon-modal"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button className="coming-soon-close" onClick={onClose}>
          ✕
        </button>

        {/* Content */}
        <div className="coming-soon-content">
          <div className="coming-soon-icon">🚀</div>
          <h2>We're Working On It</h2>
          <p>This feature is coming soon! Our team is building something amazing for you.</p>
          <div className="coming-soon-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>

        {/* Action Button */}
        <button className="coming-soon-btn" onClick={onClose}>
          Got It! ✨
        </button>
      </div>
    </div>
  );
}
