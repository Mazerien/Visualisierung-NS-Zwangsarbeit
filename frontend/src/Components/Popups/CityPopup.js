import { Popup } from "react-leaflet";

export default function CityPopup({ selected, setSelected }) {
  if (!selected?.coords) return null;

  const cities = selected.content?.cities || [];
  const isSingleCity = cities.length === 1;
  const singleCity = cities[0];

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

        {/* 1. TITLE */}
        <h2>
          {isSingleCity ? singleCity.name : selected.title}
        </h2>

        {/* 2. SINGLE CITY VIEW */}
        {isSingleCity ? (
          <h4 style={{ marginTop: "10px" }}>
            {singleCity.count} Zwangsarbeiter
          </h4>
        ) : (
          <>
            {/* 3. TEXT */}
            {selected.content?.text && (
              <p>{selected.content.text}</p>
            )}

            {/* 4. IMAGE */}
            {selected.content?.images?.[0] && (
              <img
                src={selected.content.images[0]}
                alt=""
                className="popup-image"
              />
            )}

            {/* 5. VIDEO */}
            {selected.content?.videos?.map((src, i) => (
              <video
                key={i}
                src={src}
                controls
                className="popup-video"
              />
            ))}

            {/* 6. TOTAL */}
            <h4 style={{ marginTop: "10px" }}>
              Insgesamt {selected.count} Zwangsarbeiter
            </h4>

            {/* 7. FULL CITY LIST */}
            {cities.length > 0 && (
              <ul
                style={{
                  paddingLeft: "15px",
                  maxHeight: "150px",
                  overflowY: "auto",
                  marginTop: "5px"
                }}
              >
                {cities
                  .slice()
                  .sort((a, b) => b.count - a.count)
                  .map((c, i) => (
                    <li key={i}>
                      {c.name}: {c.count}
                    </li>
                  ))}
              </ul>
            )}
          </>
        )}

      </div>
    </Popup>
  );
}