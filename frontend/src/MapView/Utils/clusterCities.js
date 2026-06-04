export function clusterCities(citiesArray, threshold = 0.5) {
  const clusters = [];

  citiesArray.forEach((city) => {
    let foundCluster = null;

    for (let cluster of clusters) {
      const dx = cluster.coords[0] - city.coords[0];
      const dy = cluster.coords[1] - city.coords[1];
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < threshold) {
        foundCluster = cluster;
        break;
      }
    }

    if (foundCluster) {
      // merge into cluster
      foundCluster.count += city.count;

      // average position
      foundCluster.coords = [
        (foundCluster.coords[0] + city.coords[0]) / 2,
        (foundCluster.coords[1] + city.coords[1]) / 2
      ];

      foundCluster.cities.push(city);
    } else {
      clusters.push({
        coords: city.coords,
        count: city.count,
        cities: [city]
      });
    }
  });

  return clusters;
}