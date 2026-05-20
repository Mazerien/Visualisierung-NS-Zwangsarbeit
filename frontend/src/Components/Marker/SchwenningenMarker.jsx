// Components/SchwenningenMarker.jsx

import { Circle } from "react-leaflet";

export default function SchwenningenMarker({ point, setSelected }) {
  if (!point?.coords) return null;

  return (
    <Circle
      center={point.coords}
      radius={20}
      pathOptions={{
        color: "#ff5500",
        fillOpacity: 0.8
      }}
      eventHandlers={{
        click: () => {
          setSelected({
            title: point.name,
            Panel: point.Panel
          });
        },

        mouseover: (e) => {
          e.target.setStyle({
            fillOpacity: 1,
            weight: 4
          });
        },

        mouseout: (e) => {
          e.target.setStyle({
            fillOpacity: 0.8,
            weight: 1
          });
        }
      }}
    />
  );
}