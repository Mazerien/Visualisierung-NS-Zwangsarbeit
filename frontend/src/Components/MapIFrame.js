export default function MapIframe({ zoom, year }) {
  return (
    <iframe
  // TODO: Ensure it checks for both online and localhost
      src={`http://backend:5000/api/osm?zoom_level=${zoom}&year=${year}`}
      title="OSM Map"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        border: "none",
      }}
      scrolling="no"
    />
  );
}
