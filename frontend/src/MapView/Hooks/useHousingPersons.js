import { useEffect, useState } from "react";
import { safeFetch } from "../Utils/safeFetch";

export function useHousingPersons(zoomLevel) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (zoomLevel === 2) {
      safeFetch(
        "https://flask.p-qsvcne.project.space/api/housing-persons",
        []
      ).then(setData);
    }
  }, [zoomLevel]);

  return data;
}