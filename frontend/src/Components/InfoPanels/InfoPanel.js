import "./InfoPanel.css";

export default function InfoPanel({ selected, onClose }) {
  const PanelComponent = selected?.Panel;

  return (
    <div className={`info-panel ${selected ? "open" : ""}`}>
      {selected && (
        <>
          <button className="edge-close" onClick={onClose}>
            ➜
          </button>

          <div className="panel-content">
            <h2>{selected.title}</h2>
            {PanelComponent && <PanelComponent />}
          </div>
        </>
      )}
    </div>
  );
}