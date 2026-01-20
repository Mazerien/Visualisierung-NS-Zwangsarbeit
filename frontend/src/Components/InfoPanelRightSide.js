export default function RightPanel({ selected, onClose }) {
  return (
    <div
      className={`info-panel ${selected ? "open" : ""}`}
      style={{
        position: "fixed",
        top: 0,
        right: 0,
        width: "400px",
        height: "100vh",
        backgroundColor: "white",
        boxShadow: "-4px 0 8px rgba(0,0,0,0.2)",
        zIndex: 1000,
        padding: "16px",
        overflowY: "auto",
        transform: selected ? "translateX(0)" : "translateX(100%)",
        transition: "transform 0.3s ease",
      }}
    >
      {selected && (
        <>
          <button
            onClick={onClose}
            style={{
              position: "absolute",
              top: 10,
              right: 10,
              cursor: "pointer",
              border: "none",
              background: "transparent",
              fontSize: "18px",
            }}
          >
            ✖
          </button>

          <h2>{selected.title}</h2>

          {selected.content.text && <p>{selected.content.text}</p>}

          {selected.content.images &&
            selected.content.images.map((src, i) => (
              <img
                key={i}
                src={src}
                alt=""
                style={{ width: "100%", margin: "8px 0", borderRadius: "6px" }}
              />
            ))}

          {selected.content.videos &&
            selected.content.videos.map((src, i) => (
              <video
                key={i}
                src={src}
                controls
                style={{ width: "100%", margin: "8px 0", borderRadius: "6px" }}
              />
            ))}
        </>
      )}
    </div >
  );
}
