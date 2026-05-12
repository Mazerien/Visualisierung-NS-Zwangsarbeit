import "./TimelineSlider.css";

const years = [1938, 2000, 2025];

export default function TimelineSlider({ year, setYear }) {
  const index = years.indexOf(year);

  const handleChange = (e) => {
    const newIndex = Number(e.target.value);
    setYear(years[newIndex]);
  };

  return (
    <div className="timeline-container">
      <div className="timeline-label">
        Jahr: <strong>{year}</strong>
      </div>

      <input
        type="range"
        min="0"
        max={years.length - 1}
        step="1"
        value={index}
        onChange={handleChange}
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