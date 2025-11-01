# Flask app
## Directory Structure
```
app/
├── database.py
├── main.py
├── static
│   └── *.css
    └── *.ico
    └── images
        └── *.png
└── templates
    ├── *.html
```
database.py defines the connection with PostgreSQL.  
main.py is the Flask app.  
map.py concerns Open Street Map API calls.  

static/ serves CSS files.  
static/images/ serves image files. Currently, map generation data gets stored here.  
templates/ serves HTML templates. All templates must inherit from `templates/base.html`.