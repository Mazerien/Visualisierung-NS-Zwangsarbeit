# API for interaction between back- and frontend
The API is called through either POST, or GET requests.  
Below is a documentation of the possible interactions with the frontend.

## Debug / Testing
### GET /api/hello
Returns Hello, World; ensures connection with backend is possible.

## OpenStreetMap
### GET /api/osm
Returns HTML string (iframe) of an OSM map.  
**Parameters:**  
- `zoom_level: int`: 0, 1, or 2. Defaults to minimum if no or wrong parameter given.

## OpenHistoryMap
### GET /api/ohm
TODO: Docstring.  
**Parameters:**
- `name: String`: Name of the city. Required field.
- `country: String`: Name of the country in English.
- `year: int`: The year in AD.