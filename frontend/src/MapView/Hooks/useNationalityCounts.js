import { useEffect, useState } from "react";

export function useNationalityCounts() {
  const [counts, setCounts] = useState({});

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:5000/api/nationality");
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