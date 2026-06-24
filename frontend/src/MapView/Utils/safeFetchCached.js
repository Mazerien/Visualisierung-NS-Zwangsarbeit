// utils/safeFetchCached.js

const memoryCache = new Map();

export async function safeFetchCached(key, url, fallback) {
  // 1. in-memory cache (fast + no limits)
  if (memoryCache.has(key)) {
    return memoryCache.get(key);
  }

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const text = await res.text();
    const data = JSON.parse(text);

    // only store in memory
    memoryCache.set(key, data);

    return data;

  } catch (err) {
    console.error("FETCH ERROR:", url, err);
    return fallback;
  }
}