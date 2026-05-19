import { MapContainer, TileLayer, GeoJSON, Polyline } from "react-leaflet";
import { useEffect, useState, useRef } from "react";
import CityCircle from "./CityCircles/CityCircle";
import CityPopup from "./Popups/CityPopup";

export default function MapView({ zoom, year,selected, setSelected}) {
  const [data, setData] = useState(null);
  const [nationalityCounts, setNationalityCounts] = useState({});
  const selectedCountryRef = useRef(null);
  
  const counts = Object.values(nationalityCounts);
  const min = counts.length ? Math.min(...counts) : 0;
  const max = counts.length ? Math.max(...counts) : 1;

  function scaleWidth(value) {
    const minWidth = 2;
    const maxWidth = 20;
    if (max === min) return (minWidth + maxWidth) / 2;

    const normalized = (value - min) / (max - min);
    return minWidth + normalized * (maxWidth - minWidth);
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:5000/api/nationality");
        const data = await res.json();
        setNationalityCounts(data);
      } catch (err) {
        console.error("Failed to load nationality data:", err);
      }
    }

    fetchData();
  }, []);
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
  //console.log("Data: " + data.arrows)

  


  const arrowsWithWidth = arrows.map((a) => {
    const value = nationalityCounts[a.start_city];

    //console.log("arrow country:", a.start_city, "value:", value);

    return {
      ...a,
      width: scaleWidth(value ?? 1)
    };
  });


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
            const name = feature.properties.NAME;
            layer.bindTooltip(feature.properties.NAME);
            const allowedCountries = new Set([
              "Germany", "France", "Italy", "Spain", "United Kingdom",
              "Poland", "Austria", "Switzerland", "Netherlands",
              "Belgium", "Czechia", "Slovakia", "Hungary",
              "Romania", "Bulgaria", "Greece", "Norway", "Sweden",
              "Finland", "Denmark", "Portugal", "Ireland",
              "Ukraine", "Belarus", "Russia"
            ]);

            const isClickable = allowedCountries.has(name);

             layer.on({
                click: (e) => {
                  if (!isClickable) return;

                  const map = e.target._map;
                  const bounds = e.target.getBounds();

                  if (selectedCountryRef.current === name) {
                    map.setView(data.view.center, data.view.zoom);
                    selectedCountryRef.current = null;
                    return;
                  }

                  map.fitBounds(bounds, {
                    padding: [20, 20],
                    maxZoom: 7
                  });

                  selectedCountryRef.current = name;
                }
              });
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
      {zoom < 2 && arrowsWithWidth.map((a, i) => (
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

      {/* -----------------------------
          POPUPS (For the Circles)
      ----------------------------- */}
      {selected && selected.coords && (
        <CityPopup selected={selected} setSelected={setSelected} />
      )}
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
