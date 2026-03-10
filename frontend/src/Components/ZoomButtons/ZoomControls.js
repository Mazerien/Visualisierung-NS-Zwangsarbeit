import ZoomButton from "./ZoomButton";
export default function ZoomControls({ zoom, setZoom, zoomLevels }) {
  return (
    <div
      style={{
        position: "fixed",
        top: "45%",
        left: "7%",
        transform: "translate(-50%, -50%)",
        zIndex: 1000,
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      {zoomLevels.map((level) => (
        <ZoomButton
          key={level}
          level={level}
          isActive={zoom === level}
          onClick={() => setZoom(level)}
        />
      ))}
    </div>
  );
}
