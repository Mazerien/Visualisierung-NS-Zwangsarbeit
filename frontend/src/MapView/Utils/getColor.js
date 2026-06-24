const colorCache = {};

export function getColor(name) {
  if (!name) return "#cccccc";
  if (colorCache[name]) return colorCache[name];

  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }

  const lightness = 70 + (Math.abs(hash) % 20); // Hier die Grau werte Ändern. In der Klammer ist der Wert für die Variirung
  const color = `hsl(0, 0%, ${lightness}%)`;

  colorCache[name] = color;
  return color;
}