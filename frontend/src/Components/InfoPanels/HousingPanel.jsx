// Panels/HousingPanel.jsx

import "./InfoPanel.css";

export default function HousingPanel({ data }) {
  if (!data) return null;

  const persons = Array.isArray(data.persons) ? data.persons : [];

  return (
    <div>
      <p><strong>Art des Ortes:</strong> {data.type || "Unknown"}</p>

      <p>
        <strong>Anzahl Personen:</strong> {data.persons_count ?? 0}
      </p>

      <ul>
        {persons.length > 0 ? (
          persons.map((p, i) => (
            <li key={i}>{p}</li>
          ))
        ) : (
          <li>No persons found</li>
        )}
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