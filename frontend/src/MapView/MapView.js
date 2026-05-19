import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import { useRef } from "react";

import CityCircle from "../Components/CityCircles/CityCircle";
import CityPopup from "../Components/Popups/CityPopup";

import CountriesLayer from "./Layers/CountriesLayer";
import { useMapData } from "./Hooks/useMapData";
import { useNationalityCounts } from "./Hooks/useNationalityCounts";
import { scaleWidth } from "./Utils/scaleWidth";

export default function MapView({ zoom, year, selected, setSelected }) {
  const data = useMapData(zoom, year);
  const nationalityCounts = useNationalityCounts();

  const selectedCountryRef = useRef(null);

  if (!data) return <div>Loading map...</div>;

  const counts = Object.values(nationalityCounts);
  const min = counts.length ? Math.min(...counts) : 0;
  const max = counts.length ? Math.max(...counts) : 1;

  const arrowsWithWidth = (data.arrows || []).map(a => ({
    ...a,
    width: scaleWidth(nationalityCounts[a.start_city] ?? 1, min, max)
  }));

  const cities = data.cities || {};
  const countries = data.countries;

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
      <TileLayer
        url={
          zoom < 2
            ? "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}"
            : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        }
      />

      {zoom < 2 && (
        <CountriesLayer
          countries={countries}
          year={year}
          data={data}
          selectedCountryRef={selectedCountryRef}
        />
      )}

      {zoom < 2 &&
        Object.entries(cities).map(([city, d]) => {
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

      {zoom < 2 &&
        arrowsWithWidth.map((a, i) => (
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

      {selected?.coords && (
        <CityPopup selected={selected} setSelected={setSelected} />
      )}
    </MapContainer>
  );
}