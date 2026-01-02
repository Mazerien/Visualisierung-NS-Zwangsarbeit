import { useState } from "react";
import ZoomControls from "./Components/ZoomControls";
import MapIframe from "./Components/MapIFrame";
import Interactable from "./Components/Interactable";
import InfoPanel from "./Components/InfoPanel";
import { interactablesData } from "./Components/InteractablesData";

function App() {
  const [zoom, setZoom] = useState(0);
  const [selected, setSelected] = useState(null);
  const zoomLevels = [0, 1, 2];
  const [interactables, setInteractables] = useState([]); // state for current zoom data

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
      <MapIframe zoom={zoom} />

      {/* Render interactables dynamically */}
      {/*{interactables.map((item) => (  // use this when using Backend data */}
      {interactablesData[zoom].map((item) => (
        <Interactable
          key={item.id}
          x={item.x}
          y={item.y}
          onClick={() => setSelected(item)}
        />
      ))}

      <InfoPanel selected={selected} onClose={() => setSelected(null)} />
    </div>
  );
}

export default App;
