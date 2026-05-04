import markerImg1 from "./Placeholder_Media/pexels-jjagtenberg-103123.jpg";
import markervid1 from "./Placeholder_Media/853889-hd_1920_1080_25fps.mp4"

export const interactablesData = {
  0: [
    {
      id: 1,
      x: 1000,
      y: 600,
      title: "Zoom 0 - Marker 1",
      content: {
        text: "This is some info text for marker 1 at zoom 0.",
        images: [markerImg1],
        videos: []
      }
    },
    {
      id: 2,
      x: 1200,
      y: 800,
      title: "Zoom 0 - Marker 2",
      content: {
        text: "Another marker with an image and video.",
        images: [markerImg1],
        videos: [markervid1]
      }
    }
  ],
  1: [
    {
      id: 3,
      x: 800,
      y: 800,
      title: "Zoom 1 - Marker 1",
      content: {
        text: "Zoom 1 marker text.",
        images: [],
        videos: []
      }
    }
  ],
  2: [
    {
      id: 4,
      x: 400,
      y: 300,
      title: "Zoom 2 - Marker 1",
      content: {
        text: "Zoom 2 marker text with image.",
        images: [markerImg1],
        videos: []
      }
    }
  ]
};
