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
import { useHousingPersons } from "./Hooks/useHousingPersons";
import { housingGeo } from "./Hooks/staticGeo";

export default function MapView({ zoom, year, selected, setSelected, panelUI, setPanelUI, selectedHousing, setSelectedHousing}) {
  const data = useMapData(zoom, year);
  const nationalityCounts = useNationalityCounts();
  const housingData = useHousingPersons(zoom);
  const enrichedHousingData = (housingData || []).map((h) => ({
    ...h,
    coords: housingGeo[h.housing_id] || null
  }));
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

  if (!data || !data.view || !data.view.center) {
    return <div>Loading map...</div>;
  }

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
  const bounds = {
    0: [
      [30.0, -10.5],
      [68.0, 40.0]
    ],

    1: [
      [38.0, -8.0],   // more room downward + west
      [60.5, 30.0]    // more room upward + east
    ],

    2: [
      [48.03, 8.48],  // more west space (this is the big fix)
      [48.11, 8.62]   // more east + a bit more south room
    ]
  };

  const ZOOM_LIMITS = {
    0: { min: 4, max: 7 },   // Europe (zoomed out)
    1: { min: 6, max: 8 },   // region / country
    2: { min: 15, max: 17 }  // city (Schwenningen)
  };

  return (
    <MapContainer
      key={`${zoom}-${year}`}
      center={data.view.center}
      zoom={data.view.zoom}
      style={{ height: "100vh", width: "100%" }}
      scrollWheelZoom={true}
      dragging={true}
      touchZoom={true}
      doubleClickZoom={false}
      keyboard={false}
      zoomControl={false}
      maxBounds={bounds[zoom]}
      maxBoundsViscosity={1.0}
      minZoom={ZOOM_LIMITS[zoom].min}  
      maxZoom={ZOOM_LIMITS[zoom].max}
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

      {zoom > 2 && arrowsWithWidth
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
      enrichedHousingData.map((housing) => (
        <SchwenningenMarker
          key={housing.housing_id}
          housing={housing}
          setPanelUI={setPanelUI}
          selectedHousing={selectedHousing}
          setSelectedHousing={setSelectedHousing}
        />
      ))}

    <div
      style={{
        position: "absolute",
        bottom: "5px",
        left: "10px",
        zIndex: 1000,
        background: "rgba(255,255,255,0.8)",
        padding: "4px 8px",
        fontSize: "11px",
        borderRadius: "4px"
      }}
    >
      © OpenStreetMap contributors | Tiles © Esri <br />
      Data: Natural Earth, historical-basemaps (A. Ourednik)
    </div>
    </MapContainer>
  );
}