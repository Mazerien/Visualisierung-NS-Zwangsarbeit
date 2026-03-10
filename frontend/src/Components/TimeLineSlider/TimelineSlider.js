import { useState } from "react";
import "./TimelineSlider.css";

export default function TimelineSlider() {
  const years = [1938, 1940, 1999, 2026];

  const [index, setIndex] = useState(0);

  return (
    <div className="timeline-container">
      <div className="timeline-label">
        Jahr: <strong>{years[index]}</strong>
      </div>

      <input
        type="range"
        min={years[0]}
        max={years[years.length - 1]}
        step="1"
        value={index}
        onChange={(e) => setIndex(Number(e.target.value))}
        className="timeline-slider"
      />

      <div className="timeline-years">
        {years.map((y) => (
          <span key={y}>{y}</span>
        ))}
      </div>
    </div>
  );
}