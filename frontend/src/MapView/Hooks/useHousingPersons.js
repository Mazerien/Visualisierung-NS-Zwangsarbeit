import { useEffect, useState } from "react";
import { safeFetchCached } from "../Utils/safeFetchCached";

export function useHousingPersons(zoomLevel) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (zoomLevel === 2) {
      safeFetchCached(
        "housing-persons",
        "https://flask.p-qsvcne.project.space/api/housing-persons",
        []
      ).then(setData);
    }
  }, [zoomLevel]);

  return data;
}