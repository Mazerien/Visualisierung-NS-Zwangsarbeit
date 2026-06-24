import { useEffect, useState } from "react";
import { safeFetchCached } from "../Utils/safeFetchCached";

export function useNationalityCounts() {
  const [counts, setCounts] = useState({});

  useEffect(() => {
    safeFetchCached(
      "Nationality-Counts",
      `https://flask.p-qsvcne.project.space/api/nationality`,
      []
    ).then(setCounts);
  }, []);

  return counts;
}