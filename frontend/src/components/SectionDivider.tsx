import "./SectionDivider.css";

type SectionDividerProps = {
  text?: string;
};

export default function SectionDivider({ text }: SectionDividerProps) {
  if (!text) {
    return <div className="section-divider-line" />;
  }

  return (
    <div className="section-divider">
      <span className="line" />

      <h2>{text}</h2>

      <span className="line" />
    </div>
  );
}