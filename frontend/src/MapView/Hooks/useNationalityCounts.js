import { useEffect, useState } from "react";
import { safeFetch } from "../Utils/safeFetch";

export function useNationalityCounts() {
  const [counts, setCounts] = useState({});

  useEffect(() => {
    safeFetch(
      "https://flask.p-qsvcne.project.space/api/nationality",
      {} // fallback
    ).then(setCounts);
  }, []);

  return counts;
}