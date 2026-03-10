import { useState } from "react";
import "./TimelineSlider.css";

export default function TimelineSlider() {
  const [year, setYear] = useState(1940);

  return (
    <div className="timeline-container">
      <div className="timeline-label">
        Jahr: <strong>{year}</strong>
      </div>

      <input
        type="range"
        min="1940"
        max="2026"
        value={year}
        onChange={(e) => setYear(Number(e.target.value))}
        className="timeline-slider"
      />

      <div className="timeline-years">
        <span>1940</span>
        <span>2026</span>
      </div>
    </div>
  );
}
