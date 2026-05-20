// data/schwenningenPoints.js

import MarktplatzPanel from "../../Components/InfoPanels/MarktplatzPanek";
import NeckarquellePanel from "../../Components/InfoPanels/NeckarquellePanel";
import CampusPanel from "../../Components/InfoPanels/CampusPanel"

export const schwenningenPoints = [
  {
    id: 1,
    name: "Marktplatz",
    coords: [48.0608, 8.5336],
    Panel: MarktplatzPanel
  },
  {
    id: 2,
    name: "Neckarquelle",
    coords: [48.0580, 8.5355],
    Panel: NeckarquellePanel
  },
  {
    id: 3,
    name: "HFU Campus",
    coords: [48.0615, 8.5305],
    Panel: CampusPanel
  }
];