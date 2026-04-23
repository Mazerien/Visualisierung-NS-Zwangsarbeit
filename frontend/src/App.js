import { useState } from "react";
import ZoomControls from "./Components/ZoomButtons/ZoomControls";
import MapIframe from "./Components/MapIFrame";
import Interactable from "./Components/Interactables/Interactable";
import InfoPanel from "./Components/InfoPanels/InfoPanelFrame/InfoPanel";
import { interactablesData } from "./Components/Interactables/InteractablesData";
import TimelineSlider from "./Components/TimeLineSlider/TimelineSlider";

function App() {
  const [zoom, setZoom] = useState(0);
  const [selected, setSelected] = useState(null);
  const zoomLevels = [0, 1, 2];
  const [year, setYear] = useState(1938);

  // For when switching to Backend Data
  /*
   useEffect(() => {
    // Fetch interactables for the current zoom from your backend
    fetch(`http://localhost:5000/api/interactables?zoom=${zoom}`)
      .then((res) => res.json())
      .then((data) => setInteractables(data))
      .catch((err) => console.error("Failed to load interactables:", err));
  }, [zoom]);*/ 
  return (
    <div>
      <ZoomControls zoom={zoom} setZoom={setZoom} zoomLevels={zoomLevels} />
      <MapIframe zoom={zoom} year={year} />

      {/* Timeout for the Animation */}
      {setTimeout(() => {
      }, 150)}
      {/*{interactables.map((item) => (  // use this when using Backend data */}
      {interactablesData[zoom].map((item) => (
        <Interactable
          key={item.id}
          x={item.x}
          y={item.y}
          onClick={() => setSelected(item)}
        />
      ))}
      <div style={{ opacity: zoom === 2 ? 0 : 1, pointerEvents: zoom === 2 ? "none" : "auto" }}>
        <TimelineSlider year={year} setYear={setYear} />
      </div>

      <InfoPanel selected={selected} onClose={() => setSelected(null)} />
    </div>
  );
}

export default App;
