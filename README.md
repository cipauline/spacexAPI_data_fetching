# Space X data ETL Pipeline

## Project overview
Fetching data from a Space X API on spaceship launches. Transforming it into a DataFrame and loading into a postgreSQL database. Automating tasks with Apache Airflow.

Project files:
- ``dags/dag.py`` - dag with tasks and their order<br>
- ``docker-compose.yaml`` - file used to define and manage docker containers<br>
- ``requirements.txt`` - text document with libraries required for the project<br>

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
