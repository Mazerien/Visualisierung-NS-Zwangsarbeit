const colorCache = {};

export function getColor(name) {
  if (!name) return "#cccccc";
  if (colorCache[name]) return colorCache[name];

  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }

  const hue = Math.abs(hash) % 360;
  const color = `hsl(${hue}, 60%, 75%)`;

  colorCache[name] = color;
  return color;
}