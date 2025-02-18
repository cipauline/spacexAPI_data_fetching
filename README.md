# SpaceX data ETL Pipeline


## Project overview
Fetching data from a SpaceX API on rocket launches. Transforming it into a DataFrame and loading into a postgreSQL database. Automating tasks with Apache Airflow, visualizing data in Tableau.

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

5. Creating an Airflow dag with extracting data from spaceX API, transforming it with pandas and loading the data into a postgres database

7. Restarting docker containers and running a dag in Airflow

8. Visualizing data in Tableau


## Visualization in Tableau

<img width="648" alt="Снимок экрана 2025-02-18 в 06 14 50" src="https://github.com/user-attachments/assets/3e9bff81-664e-402a-a03e-b97c74dccab6" />

