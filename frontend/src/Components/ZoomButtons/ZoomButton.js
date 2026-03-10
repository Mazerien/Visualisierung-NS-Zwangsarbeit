// ZoomButton.jsx
import React, { useState } from 'react';
import './ZoomButton.css';

export default function ZoomButton({ level, isActive, onClick }) {
  const [isPressed, setIsPressed] = useState(false);

  const handleClick = () => {
    // Trigger animation first
    setIsPressed(true);

    // Wait for animation duration, then update zoom
    setTimeout(() => {
      setIsPressed(false);
      onClick(); // call parent handler
    }, 100); // same as animation duration
  };

  return (
    <button
      className={`zoom-button ${isActive ? 'active' : ''} ${isPressed ? 'pulse' : ''}`}
      onClick={handleClick}
    >
      Zoom {level}
    </button>
  );
}
