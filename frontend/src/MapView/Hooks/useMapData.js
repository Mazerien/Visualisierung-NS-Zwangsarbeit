import { useEffect, useState } from "react";

export function useMapData(zoom, year) {
  const [data, setData] = useState(null);

  useEffect(() => {
    setData(null);

    fetch(`https://flask.p-qsvcne.project.space/api/osm?zoom_level=${zoom}&year=${year}`)
      .then(res => res.json())
      .then(setData)
      .catch(err => console.error("FETCH ERROR:", err));
  }, [zoom, year]);

  return data;
}