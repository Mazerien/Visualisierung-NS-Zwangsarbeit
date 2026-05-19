import { Popup } from "react-leaflet";

export default function CityPopup({ selected, setSelected }) {
  if (!selected?.coords) return null;

  return (
    <Popup
      position={selected.coords}
      className="custom-popup"
      maxWidth={400}
      offset={[0, -20]}
      eventHandlers={{
        remove: () => setSelected(null),
      }}
    >
      <div className="popup-content">
        <h2>{selected.title}</h2>

        {selected.content?.text && (
          <p>{selected.content.text}</p>
        )}

        {selected.content?.images?.[0] && (
          <img
            src={selected.content.images[0]}
            alt=""
            className="popup-image"
          />
        )}

        {selected.content?.videos?.map((src, i) => (
          <video key={i} src={src} controls className="popup-video" />
        ))}

        {selected.content?.people?.length > 0 && (
          <div style={{ marginTop: "10px" }}>
            <h4>Zwangsarbeiter: {selected.count}</h4>

            <ul style={{ paddingLeft: "15px", maxHeight: "150px", overflowY: "auto" }}>
              {selected.content.people.map((p, i) => (
                <li key={i}>
                  {p.first_name} {p.last_name}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Popup>
  );
}