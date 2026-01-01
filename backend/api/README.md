# API for interaction with the backend
The API is called through either POST, or GET requests.  
Below is a documentation of the possible interactions with the frontend.

## Debug / Testing
`/api/hello` **/GET** returns `Hello, World`; ensures connection with backend is possible.  

## Map
### OSM
`/api/osm` **/GET** returns an HTML string (iframe) of an OSM map.  
Comes with three (0, 1, 2) zoom levels specified by `zoom_level.` Defaults to minimum zoom if no or wrong parameter given.  
Parameter:  
```
zoom_level: int
```

TODO: Add current-day borders of Europe

### OHM
TODO

## Database
TODO