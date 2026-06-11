import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import { useEffect, useRef } from "react";

import CityCircle from "../Components/Marker/CityCircle";
import CityPopup from "../Components/Popups/CityPopup";

import CountriesLayer from "./Layers/CountriesLayer";
import { useMapData } from "./Hooks/useMapData";
import { useNationalityCounts } from "./Hooks/useNationalityCounts";
import { scaleWidth } from "./Utils/scaleWidth";
import { clusterCities } from "./Utils/clusterCities";
import SchwenningenMarker from "../Components/Marker/SchwenningenMarker";
import { schwenningenPoints } from "./Hooks/useStubSchwenningenPoints";
import { useHousingPersons } from "./Hooks/useHousingPersons";

export default function MapView({ zoom, year, selected, setSelected, panelUI, setPanelUI }) {
  const data = useMapData(zoom, year);
  const nationalityCounts = useNationalityCounts();
  const housingData = useHousingPersons(zoom);
  useEffect(() => {
    if (!setPanelUI) return;

    setPanelUI((prev) => {
      if (!prev || prev.status === "closed") return prev;

      return {
        ...prev,
        status: "closing"
      };
    });

    const t = setTimeout(() => {
      setPanelUI({
        status: "closed",
        data: null
      });
    }, 180);

    return () => clearTimeout(t);
  }, [zoom, setPanelUI]);

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

  const isValidGeoJSON =
      countries &&
      countries.type === "FeatureCollection" &&
      Array.isArray(countries.features);


  const cityArray = Object.entries(cities)
    .filter(([key, d]) => Array.isArray(d?.coords))
    .map(([key, d]) => ({
      id: key,                 // IMPORTANT: keep full key as ID
      name: key.split("|")[0], // display name only
      country: key.split("|")[1],
      year: key.split("|")[2],
      coords: d.coords,
       count: Number(d.count) || 0,
      source: d.source
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

      {zoom < 2 && isValidGeoJSON && (
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

      {zoom < 2 && arrowsWithWidth
        .filter(a =>
          Array.isArray(a.start?.coords) &&
          Array.isArray(a.end?.coords)
        )
        .map((a, i) => (
          <Polyline
            key={i}
            positions={[
              a.start.coords,
              a.end.coords
            ]}
            pathOptions={{
              color: a.color,
              weight: a.width,
              opacity: a.opacity
            }}
          />
        ))
      }

      {selected?.coords && (
        <CityPopup selected={selected} setSelected={setSelected} />
      )}

      {zoom === 2 &&
      housingData.map((housing) => (
        <SchwenningenMarker
          key={housing.housing_id}
          housing={housing}
          setPanelUI={setPanelUI}
        />
      ))}
    </MapContainer>
  );
}