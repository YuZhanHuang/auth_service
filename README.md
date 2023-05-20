# auth_service

Role base access control


## Installing Python (pyenv)
* We use [pyenv](https://github.com/pyenv/pyenv) for manage which version of python we use.
Here is simple installing instruction for mac user.
    ```bash
    brew update
    brew install pyenv
    ```
* Once installed,  you can easily install a specific version of Python.
  ```bash
  $ pyenv install 3.9.15
  $ pyenv versions
  * system (set by /Users/huangyuzhan/.pyenv/version)
    3.9.15
    ```
* You can set your python version which we recommend setting local Python interpreter for the project.
    ```bash
    $ pyenv local 3.9.15
    ```
## Managing Dependencies

### Poetry
* We specify poetry version 0.1.0 and install in global environment.
  ```bash
  $ pip3 install poetry
  ```
* Dependencies are managed inside the pyproject.toml file:
  ```bash
    [tool.poetry]
    name = "auth-service"
    version = "0.1.0"
    description = ""
    authors = ["YuZhanHuang"]
    readme = "README.md"
    packages = [{include = "auth_service"}]
    
    [tool.poetry.dependencies]
    python = "^3.9"
    flask = "^2.3.2"
    flask-sqlalchemy = "^3.0.3"
    flask-redis = "^0.4.0"
    flask-migrate = "^4.0.4"
    gunicorn = "^20.1.0"
    structlog = "^23.1.0"
    voluptuous = "^0.13.1"
    flask-security = "^3.0.0"
    
    
    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"

  ```
* To add new dependency, simply run:
  ```bash
  $ poetry add [--dev] <package name>
  ```
  > The `--dev` flag indicates that the dependency is meant to be used in development mode only. Development dependencies are not installed by default.

## How to start our project

### Setup Environment Variable for Develop
create an `.env` file in root directory of project.
```dotenv
FLASK_DEBUG=1
FLASK_ENV=development
SECRET_KEY=5566neverdie
JWT_SECRET_KEY=TurningRed
MAIL_USERNAME=joe@gmail.com
MAIL_PASSWORD=***********
DB_USER=joe
DB_PASS=19921119
DB_HOST=auth_service_db
DB_NAME=postgres
REDIS_HOST=auth_service_redis
REDIS_POST=6379
```

### Services Are Containerized
> docker-compose.yml is in the root directory of project. 
* start services
  ```angular2html
  $ docker-compose up -d [--build]
  ```
  > `--build` is optional flag
* List all services by command
  ```bash
  $ docker-compose ps
  ```
* Checking each service log
  ```bash
  $ docker-compose logs -f <service name>
  ```