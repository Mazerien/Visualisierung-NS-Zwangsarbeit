# Visualization of the International Dimension of Forced Labour in Nazi Germany
## Setup
### dotenv
Copy and rename `.env.example` into `.env` and set the secrets you want.  
### Docker
`docker compose up -d` to automatically install and start all Docker containers (Directus; MySQL; Python).

## Directory structure
`backend/`: Flask backend.  
`frontend/`: React frontend. (WIP)  
`scripts/`: Auxilliary scripts such as importing the data into the MySQL/Directus DB.  

# Sources
[Directus docker-compose](https://directus.io/docs/self-hosting/deploying)  
[MySQL docker-compose](https://hub.docker.com/_/mysql/)  
[Python docker-compose](https://tecadmin.net/how-to-create-and-run-a-flask-application-using-docker/)
