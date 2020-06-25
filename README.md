# EagleEYE Web Service APIs
This Web Service APIs was built based on my own public repository, [Flask-API](https://github.com/ardihikaru/flask-api), 
is using RestfulAPI as the communication protocol between the Server and the connected Client(s).


## TO DO LIST

- [x] Base code: [Flask App + Swagger UI](https://github.com/ardihikaru/flask-api)
- [x] APIs (**FYI: Temporary disabled the security access: No `access_token` required**)
    - [x] Auth
        - [x] `POST /auth/login`: Login and receive `access_token`
        - [x] `GET /auth/logout`: Logout and delete active `access_token`
    - [x] Users
        - [x] `POST /users`: Register a new user 
        - [x] `GET /users`: Get all users
        - [x] `GET /users/<username>`: Get a specific user
        - [x] `DELETE /users/<username>`: Delete a specific user
    - [x] Drones
        - [x] `POST /drones`: Register a new drone 
        - [x] `GET /drones`: Get all drones
        - [x] `DELETE /drones`: Delete all drones
        - [x] `DELETE /drones/<drone_id>`: Delete a specific drone
    - [x] Worker Nodes
        - [x] `POST /workers`: Register a new worker node
        - [x] `GET /workers`: Get all worker nodes
        - [x] `DELETE /workers`: Delete all worker nodes
        - [ ] `DELETE /workers/<worker_id>`: Delete a specific worker node
    - [x] Frames
        - [x] `POST /frames`: Insert a new image frame
        - [x] `GET /frames`: Get all image frames
        - [x] `DELETE /frames`: Delete all image frames
    - [x] CPU utilization
        - [x] `POST /util/cpu/cores`: Add current (timestamp) CPU Cores utilization (in percent)
        - [x] `GET /util/cpu/cores/<num_records>`: Get last N records of CPU Cores utilization (in percent)
        - [x] `POST /util/cpu/rams`: Add current (timestamp) CPU RAMs utilization (in GB)
        - [x] `GET /util/cpu/rams/<num_records>`: Get last N records of CPU RAMs utilization (in GB)
    - [x] GPU utilization
        - [x] `POST /util/gpu/rams`: Add current (timestamp) GPU RAMs utilization (in GB)
        - [x] `GET /util/gpu/rams/<num_records>`: Get last N records of GPU RAMs utilization (in GB)
- [ ] Complete documentation

## Technology used in this projects (Requirements)
1. [Python 3](https://www.python.org/download/releases/3.0/)
2. [Python Flask](https://flask.palletsprojects.com/en/1.1.x/)
3. [Swagger UI](https://swagger.io/tools/swagger-ui/)
4. [Redis Database](https://redis.io/)
5. [Cockroach Database](https://www.cockroachlabs.com/)
6. [Elasticsearch Database](https://www.elastic.co/elasticsearch/)
7. [Kibana](https://www.elastic.co/kibana)

## Installation
1. Python library 
    ```
    pip install -r requirements.txt
    ```
2. Install Redis Database
    1. Install docker.io
    2. Install redis-tools
    3. Go to redis directory: `$ cd others/redis`
    4. Install `Dockerfile`: `$ docker build -t 5g-dive/redis:1.0 .`
    5. Instantiate redis container: `. run.sh`
    5. Test insert data into RedisDB: `. test.sh`
3. Install Coachroach Database
    - [MAC OS](https://kb.objectrocket.com/cockroachdb/how-to-install-cockroachdb-on-mac-os-x-307)
    - [WINDOWS](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html)
    - [LINUX](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html)
4. Configure CockroachDB:
    1. Follow step [here](https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html) and [here](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html)
    2. Add new user:
        - login: `$ cockroach sql --certs-dir=certs --host=localhost:26257`
        - Create new database: `CREATE DATABASE eagleeyedb;`
        - Create new user: 
            - Insecure Mode: `CREATE USER eagleeyeuser;`
            - Secure Mode: `CREATE USER eagleeyeuser WITH PASSWORD 'bismillah';`
        - Grant user the database access: `GRANT ALL ON DATABASE eagleeyedb TO eagleeyeuser;`
    3. Generate cert (Secure mode **ONLY**): `cockroach cert create-client flaskuser --certs-dir=certs --ca-key=my-safe-directory/ca.key`
5. Install and Configure Elasticsearch Database:
    - [Follow steps here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
6. Install and Configure Kibana:
    - [Follow steps here](https://www.elastic.co/guide/en/kibana/current/install.html)

## How to use: <TBD>
1. Run RedisDB
2. Run CoachroachDB
    - [Insecure](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html) (For newbie):
        - RUN: `$ cockroach start --insecure --listen-addr=localhost`
        - Login SQL: `$ cockroach sql --insecure`
    - [Secure](https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html) (Recommended):
        - RUN: <Please follow the steps from the given link above>
            - Node 1: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node1 \
                    --listen-addr=localhost:26257 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
            - Node 2: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node2 \
                    --listen-addr=localhost:26258 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
            - Node 3: 
                ``` 
                cockroach start \
                    --certs-dir=certs \
                    --store=node3 \
                    --listen-addr=localhost:26259 \
                    --http-addr=localhost:8080 \
                    --join=localhost:26257,localhost:26258,localhost:26259 \
                    --background
                ```
             - Run `Secure Mode`: `$ cockroach init --certs-dir=certs --host=localhost:26257`
                - Check status: `$ grep 'node starting' node1/logs/cockroach.log -A 11` 
        - Login SQL: `$ cockroach sql --certs-dir=certs --host=localhost:26257`
3. Run Flask Web Service

## Database: Redis Database
RedisDB used only to store JWT-related information
         
## Accessible APIs 
* Auth
    - `POST /auth/login`: Login and receive `access_token`
    - `GET /auth/logout`: Logout and delete active `access_token`
* Users
    - `POST /users`: Register a new user 
    - `GET /users`: Get all users
    - `GET /users/<username>`: Get a specific user
    - `DELETE /users/<username>`: Delete a specific user
* Drones
    - `POST /drones`: Register a new drone 
    - `GET /drones`: Get all drones
    - `DELETE /drones`: Delete all drones
    - `DELETE /drones/<drone_id>`: Delete a specific drone
* Worker Nodes
    - `POST /workers`: Register a new worker node
    - `GET /workers`: Get all worker nodes
    - `DELETE /workers`: Delete all worker nodes
    - [ ] `DELETE /workers/<worker_id>`: Delete a specific worker node
* Frames
    - `POST /frames`: Insert a new image frame
    - `GET /frames`: Get all image frames
    - `DELETE /frames`: Delete all image frames
* CPU utilization
    - `POST /util/cpu/cores`: Add current (timestamp) CPU Cores utilization (in percent)
    - `GET /util/cpu/cores/<num_records>`: Get last N records of CPU Cores utilization (in percent)
    - `POST /util/cpu/rams`: Add current (timestamp) CPU RAMs utilization (in GB)
    - `GET /util/cpu/rams/<num_records>`: Get last N records of CPU RAMs utilization (in GB)
* GPU utilization
    - `POST /util/gpu/rams`: Add current (timestamp) GPU RAMs utilization (in GB)
    - `GET /util/gpu/rams/<num_records>`: Get last N records of GPU RAMs utilization (in GB)

### Response

```javascript
{
  "status"  : bool,
  "message" : string,
  "results" : `LIST` or `DICT`
}
```

## Status Codes

This Web Service returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 401 | `Unauthorized Access. Access Token should be provided and validated.` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

NB: More detail information regarding API Documentation please refer to [Here](https://gitlab.com/idn-games/idn-games-web-service/app/controllers/api/README.md).

## Contributing
Self-Maintained. If there any issue, please do not hesitate to contact me. 

## Contributors
1. Muhammad Febrian Ardiansyah, https://github.com/ardihikaru

## Extra resources
1. **Thread** with `concurrent.futures`; https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
2. **Flask Restplus** in **HTTPS** ; https://stackoverflow.com/questions/47508257/serving-flask-restplus-on-https-server

## License
[MIT](https://choosealicense.com/licenses/mit/)