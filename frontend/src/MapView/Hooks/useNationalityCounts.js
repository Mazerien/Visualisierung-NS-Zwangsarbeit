import { useEffect, useState } from "react";

export function useNationalityCounts() {
  const [counts, setCounts] = useState({});

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("https://flask.p-qsvcne.project.space/api/nationality");
        const data = await res.json();
        setCounts(data);
      } catch (err) {
        console.error("Failed to load nationality data:", err);
      }
    }

    fetchData();
  }, []);

  return counts;
}