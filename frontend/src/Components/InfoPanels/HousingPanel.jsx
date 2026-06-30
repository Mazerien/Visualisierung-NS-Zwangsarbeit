// Panels/HousingPanel.jsx

import "./InfoPanel.css";

export default function HousingPanel({ data }) {
  if (!data) return null;

  const persons = Array.isArray(data.persons) ? data.persons : [];
  const fotos = Array.isArray(data.fotos) ? data.fotos : [];

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

      {fotos.length > 0 && (
        <div className="panel-images">
          {fotos.map((url, i) => (
            <img
              key={i}
              src={url}
              alt={`${data.name_place || "Housing"} ${i + 1}`}
              className="panel-image"
            />
          ))}
        </div>
      )}
    </div>
  );
}