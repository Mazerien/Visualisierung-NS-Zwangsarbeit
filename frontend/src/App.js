// App.js
import './App.css';
import { useState } from 'react';
import ZoomButton from './Components/ZoomButton';
import Interactable from './Components/Interactable';
import { interactablesData } from './Components/InteractablesData';

function App() {
  const [zoom, setZoom] = useState(0); // initial zoom level

  // List of zoom levels you want buttons for
  const zoomLevels = [0, 1, 2];

  return (
    <div>
      {/* Buttons container */}
      <div style={{
        position: "fixed",
        top: "40%",
        left: "5%",
        zIndex: 1000,
        display: "flex",
        flexDirection: "column",
        gap: "10px"
      }}>
        {zoomLevels.map(level => (
          <ZoomButton
            key={level}
            level={level}
            isActive={zoom === level}
            onClick={() => setZoom(level)}
          />
        ))}
      </div>

      {/* Map iframe */}
      <iframe
        src={`http://localhost:5000/api/osm?zoom_level=${zoom}`}
        title="OSM Map"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          border: "none",
          display: 'block',
        }}
      />
    {/* Interactables for current zoom */}
      {interactablesData[zoom].map(interactable => (
        <Interactable
          key={interactable.id}
          x={interactable.x}
          y={interactable.y}
          title={interactable.title}
          content={interactable.content}
        />
      ))}
    </div>
  );
}

export default App;
