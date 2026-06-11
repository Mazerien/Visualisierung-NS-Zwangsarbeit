import { Circle } from "react-leaflet";
import HousingPanel from "./InfoPanels/HousingPanel";

export default function SchwenningenMarker({ housing, setPanelUI }) {
  console.log(housing.coords);
  if (!housing?.coords) return null;

  return (
    <Circle
      center={housing.coords}
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
                title: housing.name_place,
                Panel: HousingPanel,
                props: {
                  data: housing
                }
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