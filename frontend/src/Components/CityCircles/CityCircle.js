import { Circle } from "react-leaflet";

export default function CityCircle({ city, data, setSelected }) {
  if (!data?.coords) return null;

  return (
    <Circle
      center={data.coords}
      radius={Math.max(5000, Math.sqrt(data.count) * 8000)}
      pathOptions={{
        color: "#3388ff",
        fillOpacity: 0.6
      }}

      eventHandlers={{
        click: () => {
          setSelected({
            title: city,
            content: {
              text: `Zwangsarbeiter Herkunft: ${data.count}`,
              images: [],
              videos: []
            },
            coords: data.coords,
            count: data.count
          });
        },

        mouseover: (e) => {
          e.target.setStyle({
            fillOpacity: 0.9,
            weight: 3
          });
        },

        mouseout: (e) => {
          e.target.setStyle({
            fillOpacity: 0.6,
            weight: 1
          });
        }
      }}
    />
  );
}