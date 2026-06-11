import { GeoJSON } from "react-leaflet";
import { getColor } from "../Utils/getColor";

export default function CountriesLayer({
  countries,
  year,
  data,
  selectedCountryRef
}) {
  if (!countries) return null;

  const allowedCountries = new Set([
    "Germany", "France", "Italy", "Spain", "United Kingdom",
    "Poland", "Austria", "Switzerland", "Netherlands",
    "Belgium", "Czechia", "Slovakia", "Hungary",
    "Romania", "Bulgaria", "Greece", "Norway", "Sweden",
    "Finland", "Denmark", "Portugal", "Ireland",
    "Ukraine", "Belarus", "Czechoslovakia", "Yugoslavia",
    "Albania", "Turkey", "Germany (France)", "Germany (UK)",
    "Germany (USA)", "Germany (Soviet)", "Luxembourg",
    "Slovenia", "Croatia", "Serbia", "Kosovo", "Montenegro",
    "North Macedonia", "Moldova"
  ]);

  return (
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
        layer.bindTooltip(name);

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
  );
}