export function scaleWidth(value, min, max) {
  const minWidth = 2;
  const maxWidth = 20;

  if (max === min) return (minWidth + maxWidth) / 2;

  const normalized = (value - min) / (max - min);
  return minWidth + normalized * (maxWidth - minWidth);
}