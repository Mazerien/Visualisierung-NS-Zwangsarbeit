import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import { useRef } from "react";

import CityCircle from "../Components/CityCircles/CityCircle";
import CityPopup from "../Components/Popups/CityPopup";

import CountriesLayer from "./Layers/CountriesLayer";
import { useMapData } from "./Hooks/useMapData";
import { useNationalityCounts } from "./Hooks/useNationalityCounts";
import { scaleWidth } from "./Utils/scaleWidth";
import { clusterCities } from "./Utils/clusterCities";

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

  const cityArray = Object.entries(cities)
    .filter(([name, d]) => d?.coords && name !== "Unknown")
    .map(([name, d]) => ({
      name,
      ...d
    }));

  const threshold = zoom === 0 ? 1 : zoom === 1 ? 0.5 : 0;
  const clusteredCities = clusterCities(cityArray, threshold);

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
        clusteredCities.map((cluster, i) => {
          if (!cluster?.coords) return null;
          return (
            <CityCircle
              key={i}
              city={cluster.cities[0].name}
              data={{
                coords: cluster.coords,
                count: cluster.count,
                cities: cluster.cities
              }}
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