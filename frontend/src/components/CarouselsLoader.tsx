import "./CarouselsLoader.css";

interface Props {
  message?: string;
}

export default function CarouselsLoader({
  message = "Refreshing your recommendations…",
}: Props) {
  return (
    <div className="carousels-loader" role="status" aria-live="polite">
      <div className="carousels-loader__label">
        <span aria-hidden="true">✨</span>
        <span>{message}</span>
      </div>
      <div className="carousels-loader__bar">
        <div className="carousels-loader__bar-fill" />
      </div>
    </div>
  );
}
