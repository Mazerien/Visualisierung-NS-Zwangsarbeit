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

## Sources
### Docker and docker-compose
[Directus docker-compose](https://directus.io/docs/self-hosting/deploying)  
[MySQL docker-compose](https://hub.docker.com/_/mysql/)  
[Python docker-compose](https://tecadmin.net/how-to-create-and-run-a-flask-application-using-docker/)  
[Control startup and shutdown order in Compose](https://docs.docker.com/compose/how-tos/startup-order/)  
[Directus Admin user](https://directus.io/docs/configuration/general#first-admin-user)  
[MySQL health check](https://stackoverflow.com/questions/42567475/docker-compose-check-if-mysql-connection-is-ready)