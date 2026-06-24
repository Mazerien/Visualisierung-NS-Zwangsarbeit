import { useEffect, useState } from "react";
import { safeFetchCached } from "../Utils/safeFetchCached";

const fallbackMap = {
  countries: {},
  cities: {},
  arrows: [],
  view: {
    center: [44, 9],
    zoom: 5
  }
};

export function useMapData(zoom, year) {
  const [data, setData] = useState(null);

  useEffect(() => {
    setData(null);

    safeFetchCached(
      `map-${zoom}-${year}`,
      `https://flask.p-qsvcne.project.space/api/osm?zoom_level=${zoom}&year=${year}`,
      fallbackMap
    ).then(setData);

  }, [zoom, year]);

  return data;
}