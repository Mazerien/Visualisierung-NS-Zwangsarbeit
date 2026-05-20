import { Circle } from "react-leaflet";

export default function SchwenningenMarker({ point, setPanelUI }) {
  if (!point?.coords) return null;

  return (
    <Circle
      center={point.coords}
      radius={50}
      pathOptions={{
        color: "#ff5500",
        fillOpacity: 0.8
      }}
      eventHandlers={{
        click: () => {
          setPanelUI((prev) => ({
            status: "closing",
            data: prev.data
          }));

          setTimeout(() => {
            setPanelUI({
              status: "open",
              data: {
                title: point.name,
                Panel: point.Panel
              }
            });
          }, 180);
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