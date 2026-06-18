import { Circle } from "react-leaflet";

export default function CityCircle({ city, data, setSelected }) {
  if (!data?.coords) return null;

  return (
    <Circle
      center={data.coords}
      radius={Math.max(5000, Math.sqrt(data.count || 0) * 8000)}
      pathOptions={{
        color: "#8A2D2D",
        fillColor: "#8A2D2D",
        fillOpacity: 0.9
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
        },

        mouseover: (e) => {
          e.target.setStyle({
            fillOpacity: 0.9,
            weight: 6
          });
        },

        mouseout: (e) => {
          e.target.setStyle({
            fillOpacity: 1,
            weight: 1
          });
        }
      }}
    />
  );
}