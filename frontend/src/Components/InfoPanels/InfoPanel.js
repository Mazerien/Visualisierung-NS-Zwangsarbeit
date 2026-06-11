import "./InfoPanel.css";

export default function InfoPanel({ panelUI, setPanelUI }) {
  const PanelComponent = panelUI?.data?.Panel;

  const closePanel = () => {
    setPanelUI((prev) => ({ ...prev, status: "closing" }));

    setTimeout(() => {
      setPanelUI({ status: "closed", data: null });
    }, 180);
  };

  return (
    <div className={`info-panel ${panelUI.status}`}>
      {panelUI.data && (
        <>
          <button className="edge-close" onClick={closePanel}>
            ➜
          </button>

          <div className="panel-content">
            <h2>{panelUI.data.title}</h2>

            {PanelComponent && <PanelComponent {...panelUI.data.props} />}
          </div>
        </>
      )}
    </div>
  );
}