// Interactable.jsx
import React from "react";
import "./Interactable.css";

export default function Interactable({ x, y, onClick }) {
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: x,
      }}
    >
      <button className="interactable-button" onClick={onClick}>
        i
      </button>
    </div>
  );
}
