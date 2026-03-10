import React, { useState } from 'react';
import './ZoomButton.css';

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
      Zoom {level}
    </button>
  );
}
