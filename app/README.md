# Flask app
## Directory Structure
```
app/
├── database.py
├── main.py
├── geography.py
├── data  
    ├── *.json
    └── *.xlsx
├── static  
│   ├── *.css
│   ├── *.ico
│   └── images
│       └── *.png
└── templates
    └── *.html
```
database.py defines the connection with MySQL.  
main.py is the Flask app.  
geography.py concerns Open Street Map API calls.  

data/ is for data to be digitalized, for example Excel spreadsheets.  
static/ serves CSS files.  
static/images/ serves image files. Currently, map generation data gets stored here.  
templates/ serves HTML templates. All templates must inherit from `templates/base.html`.