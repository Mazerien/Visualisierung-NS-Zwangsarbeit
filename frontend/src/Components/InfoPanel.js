import "./InfoPanel.css";

export default function RightPanel({ selected, onClose }) {
  return (
    <div className={`info-panel ${selected ? "open" : ""}`}>
      {selected && (
        <>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>

          <h2>{selected.title}</h2>

          {selected.content.text && <p>{selected.content.text}</p>}

          <div className="image-text-row">
            <img
              src={selected.content.images[0]}
              alt=""
              className="panel-image large"
            />

            <div className="side-text">
              <p>This is a Man that stands</p>
            </div>
          </div>


          {selected.content.videos &&
            selected.content.videos.map((src, i) => (
              <video
                key={i}
                src={src}
                controls
                className="panel-video"
              />
            ))}
        </>
      )}
    </div>
  );
}
