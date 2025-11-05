## Visualization of the International Dimension of Forced Labour in Nazi Germany
This is a Python/Flask app listening on port TCP/5000.  
All terminal commands are run from project root directory unless stated otherwise.  

## Config
Create a Python Virtual Environment using Python >=3.12.  
Use the recommended extensions from `.vscode/extensions.json` if you use VSCode.  
Install dependencies: `pip install -r requirements.txt`  
Add new module dependencies: `pip freeze > requirements.txt`  
Add dependencies to pyproject.toml: `uv add -r requirements.txt`  

## Run Flask
Run with `flask --app app/main.py run`  
Debug mode with `flask --app app/main.py run --debug`  
Open with: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
Debug mode enables on-the-fly changes to the app as well as additional logging statements through Flask.logger.info().  

## Containerization
Install Docker and docker-compose.  
Current containerization supports an empty PostgreSQL database on TCP/5432 as well as the Flask app on TCP/5000.  
TODO: Write docker-compose for MySQL  
Create container: `docker compose up --build`  
Run container: `docker compose up -d`  
Remove container: `docker compose down`  


## Dotenv Schema
Create these files and fill them with data.  
### .env
```
SQL_USER=
SQL_PASSWORD=
SQL_DB=
SQL_HOST=
```

## OpenStreetMap
OpenStreetMap has a public API.  
This project uses the [OSMnx Python library](https://osmnx.readthedocs.io/en/stable/getting-started.html).  
As of right now, it is possible to render a high-resolution PNG image of a chosen city's roads from OSM within the Flask app.

## Sources
[Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)  
[Primer on Jinja Templating](https://realpython.com/primer-on-jinja-templating/)  
[Dockerizing Flask App with Postgres: A Step-by-Step Guide](https://medium.com/@pooya.oladazimi/dockerizing-flask-app-with-postgres-a-step-by-step-guide-e9fc9939deff)  
[Python Docker image documentation](https://hub.docker.com/_/python/)  
Boeing, G. (2025). [Modeling and Analyzing Urban Networks and Amenities with OSMnx.](https://doi.org/10.1111/gean.70009) Geographical Analysis 57 (4), 567-577. doi:10.1111/gean.70009  
[Creating beautiful maps with Python](https://towardsdatascience.com/creating-beautiful-maps-with-python-6e1aae54c55c/)
[MySQL doc](https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html)