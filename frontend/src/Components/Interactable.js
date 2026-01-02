// Interactable.jsx
import React, { useState } from "react";
import './Interactable.css';

export default function Interactable({ x, y, title, content }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className="interactable"
      style={{
        position: "absolute",
        top: y,
        left: x,
      }}
    >
      {/* Small button on the map */}
      <button
        className="interactable-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        i
      </button>

      {/* Info window */}
      {isOpen && (
        <div className="interactable-info">
          <h4>{title}</h4>
          <p>{content}</p>
        </div>
      )}
    </div>
  );
}
