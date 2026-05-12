import { MapContainer, TileLayer, GeoJSON, Polyline } from "react-leaflet";
import { useEffect, useState } from "react";
import CityCircle from "./CityCircles/CityCircle";

export default function MapView({ zoom, year, setSelected }) {
  const [data, setData] = useState(null);

  // -----------------------------
  // FETCH DATA
  // -----------------------------
  useEffect(() => {
    setData(null); // forces clean switch between modes

    fetch(`http://localhost:5000/api/osm?zoom_level=${zoom}&year=${year}`)
      .then(res => res.json())
      .then(data => {
        setData(data);
      })
      .catch(err => console.error("FETCH ERROR:", err));
  }, [zoom, year]);

  if (!data) return <div>Loading map...</div>;

  const cities = data.cities || {};
  const arrows = data.arrows || [];
  const countries = data.countries || null;

  return (
    <MapContainer
      key={`${zoom}-${year}`} 
      center={data.view.center}
      zoom={data.view.zoom}
      style={{ height: "100vh", width: "100%" }}
      scrollWheelZoom={false}
      dragging={false}
      doubleClickZoom={false}
      touchZoom={false}
      keyboard={false}
      zoomControl={false}
    >

      {zoom < 2 ? (
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}"
        />
      ) : (
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      )}

      {/* -----------------------------
          COUNTRIES (WORLD MODE ONLY)
      ----------------------------- */}
      {zoom < 2 && countries && (
        <GeoJSON
          key={`countries-${year}`}
          data={countries}
          style={(feature) => ({
            fillColor: getColor(feature.properties.NAME),
            color: "black",
            weight: 1,
            fillOpacity: 0.7
          })}
          onEachFeature={(feature, layer) => {
            layer.bindTooltip(feature.properties.NAME);
          }}
        />
      )}

      {/* -----------------------------
          CIRCLES (CITY DATA - ALWAYS)
      ----------------------------- */}
      {zoom < 2 && Object.entries(cities).map(([city, d]) => {
        if (!d?.coords || city === "Unknown") return null;
        

        return (
          <CityCircle
            key={city}
            city={city}
            data={d}
            setSelected={setSelected}
          />
        );
      })}

      {/* -----------------------------
          ARROWS (WORLD MODE ONLY)
      ----------------------------- */}
      {zoom < 2 && arrows.map((a, i) => (
        <Polyline
          key={i}
          positions={[a.start, a.end]}
          pathOptions={{
            color: a.color,
            weight: a.width,
            opacity: a.opacity
          }}
        />
      ))}

    </MapContainer>
  );
}

// -----------------------------
// COUNTRY COLORS
// -----------------------------
const colorCache = {};

function getColor(name) {
  if (!name) return "#cccccc";

  if (colorCache[name]) return colorCache[name];

  // simple hash
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }

  const hue = Math.abs(hash) % 360;

  const color = `hsl(${hue}, 60%, 75%)`;

  colorCache[name] = color;
  return color;
}