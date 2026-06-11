// Panels/HousingPanel.jsx

import "./InfoPanel.css";

export default function HousingPanel({ data }) {
  if (!data) return null;

  return (
    <div className="info-panel">
      <h3>{data.name_place || "Unknown place"}</h3>
      <p><strong>Type:</strong> {data.type || "Unknown"}</p>

      <p>
        <strong>Persons:</strong> {data.persons_count ?? 0}
      </p>

      <ul>
        {data.persons.map((p, i) => (
          <li key={i}>{p || "Unknown person"}</li>
        ))}
      </ul>
      
      {data.foto && (
        <img
            src={data.foto}
            alt={data.name_place || "Housing image"}
            className="panel-image"
        />
        )}
    </div>
  );
}