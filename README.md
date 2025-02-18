# Space X data ETL Pipeline


## Project overview
Fetching data from a Space X API on spaceship launches. Transforming it into a DataFrame and loading into a postgreSQL database. Automating tasks with Apache Airflow.

Project files:
- ``dags/dag.py`` - dag with tasks and their order<br>
- ``docker-compose.yaml`` - file used to define and manage docker containers<br>
- ``requirements.txt`` - text document with libraries required for the project<br>


## Creation process

1. Following instructions from Airflow on running Airflow in Docker (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

  Fetching docker-compose.yaml:
  ```bash
  curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'

  ```

  Initializing an airflow server (also creates a user account):
  ```bash
  docker compose up airflow-init

  ```

3. Updating a docker-compose file by adding ports to postgres service and adding a pgadmin service
   

5. Creating a postgres database in pgadmin

7. Starting a docker container

  ```bash
  docker compose up airflow-init

  ```

9. Creating a connection for a database in Airflow 

5. Creating an Aifdlow dag with extracting data from spaceX API, transforming it with pandas and loading the data into a postgres database

7. Restarting docker containers and starting a dag


## How to run a project
### run using docker:

! Ensure Docker is running locally
  

- Build an image

```bash
docker build -t etl_pipeline .

```

- Run the etl

```bash
docker run -d --name etl-container etl_pipeline

```
