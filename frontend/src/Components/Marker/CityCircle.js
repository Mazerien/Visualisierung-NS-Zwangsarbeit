import { Circle, Tooltip } from "react-leaflet";
import "./CityCircle.css";

export default function CityCircle({ city, data, setSelected }) {
  if (!data?.coords) return null;

  const radius = Math.max(15000, Math.sqrt(data.count || 1) * 12000);
  const fontSize =
    data.count > 999 ? "7px" :
    data.count > 99 ? "8px" :
    "9px";

  return (
    <Circle
      center={data.coords}
      radius={radius}
      pathOptions={{
        color: "#8A2D2D",
        fillColor: "#8A2D2D",
        fillOpacity: 0.75
      }}
      eventHandlers={{
        click: () => {
          setSelected({
            title: `${data.cities?.length || 1} Städte`,
            content: {
              count: data.count,
              images: [],
              videos: [],
              people: data.people || [],
              cities: data.cities || []
            },
            coords: data.coords,
            count: data.count,
          });
        }
      }}
    >
      <Tooltip
        permanent
        direction="center"
        className="city-label-tooltip"
      >
        <span style={{ fontSize }}>{data.cities?.length || 1}</span>
      </Tooltip>
    </Circle>
  );
}