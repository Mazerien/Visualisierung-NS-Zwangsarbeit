import { Circle } from "react-leaflet";
import HousingPanel from "../InfoPanels/HousingPanel";

export default function SchwenningenMarker({ housing, setPanelUI, selectedHousing, setSelectedHousing }) {
  console.log(housing.coords);
  if (!housing?.coords) return null;

  const isSelected = selectedHousing?.housing_id === housing.housing_id;


  return (
    <Circle
      center={housing.coords}
      radius={50}
      pathOptions={{
        color: isSelected ? "#007bff" : "#ff5500",
        fillOpacity: isSelected ? 1 : 0.8
      }}
      eventHandlers={{
        click: () => {
          setSelectedHousing(housing);
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