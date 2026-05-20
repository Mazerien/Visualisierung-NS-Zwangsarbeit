// Components/RightPanel.jsx

import "./InfoPanel.css";

export default function InfoPanel({ selected, onClose }) {
  const PanelComponent = selected?.Panel;

  return (
    <div className={`info-panel ${selected ? "open" : ""}`}>
      {selected && (
        <>
          <button className="close-button" onClick={onClose}>
            ➜
          </button>

          <h2>{selected.title}</h2>

          {PanelComponent && <PanelComponent />}
        </>
      )}
    </div>
  );
}