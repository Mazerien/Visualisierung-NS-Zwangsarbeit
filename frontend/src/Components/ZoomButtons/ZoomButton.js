import React, { useState } from 'react';
import './ZoomButton.css';

const ZOOM_LABELS = {
  0: 'Europa',
  1: 'West Europa',
  2: 'Schwenningen',
};

export default function ZoomButton({ level, isActive, onClick }) {
  const [isPressed, setIsPressed] = useState(false);

  const handleClick = () => {
    
    setIsPressed(true);

    setTimeout(() => {
      setIsPressed(false);
      onClick(); 
    }, 100);
  };

  return (
    <button
      className={`zoom-button ${isActive ? 'active' : ''} ${isPressed ? 'pulse' : ''}`}
      onClick={handleClick}
    >
      {ZOOM_LABELS[level] ?? `Zoom ${level}`}
    </button>
  );
}
