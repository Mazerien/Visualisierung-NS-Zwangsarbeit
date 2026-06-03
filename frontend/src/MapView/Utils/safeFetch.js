// utils/safeFetch.js

export async function safeFetch(url, fallback) {
  try {
    const res = await fetch(url);

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const text = await res.text();

    try {
      return JSON.parse(text);
    } catch {
      throw new Error("Invalid JSON (HTML returned)");
    }

  } catch (err) {
    console.error("FETCH ERROR:", url, err);

    return fallback;
  }
}