# Authentication with Flask, React, and Docker

https://testdriven.io/courses/auth-flask-react/

## Local

Creation

```bash
docker-compose up -d --build
```

### Backend

Access

```bash
docker-compose exec api flask shell
```

Initialize

```bash
docker-compose exec api python manage.py recreate_db

docker-compose exec api python manage.py seed_db
```

Lint

```bash
docker-compose exec api flake8 src

docker-compose exec api black src

docker-compose exec api isort src
```

Test

```bash
docker-compose exec api python -m pytest "src/tests" -p no:warnings

docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src"

docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src" --cov-report html
```

Functional Tests

```
http GET http://localhost:5004/users
http --json POST http://localhost:5004/users username=someone email=someone@something.com
http --json PUT http://localhost:5004/users/3 username=foo email=foo@bar.com
http DELETE http://localhost:5004/users/3

http --json POST http://localhost:5004/auth/login email=michael@mherman.org password=supersecret | jq -r '"Bearer \(.access_token)"'
```

Database Access

```bash
docker-compose exec api-db psql -U postgres
# \c api_dev
# select * from users;
```

### Frontend

Add some node modules

```bash
npm install --save react-scripts
npm install --save-dev @testing-library/react@13.1.1
```

Initialize:

_I'm having issues with WSL being slow as hell, so I'm running the server from PWSH until the course moves it to docker... hopefully._

```bash
npm start
```

Testing:

```
# This will run in "watch" mode and rerun on any file change
npm test
# Get some test coverage with:
npm run coverage
```

```bash
docker-compose exec client npm test

docker-compose exec client npm run coverage
```

Linting:

```bash
docker-compose exec client npm run prettier:check

docker-compose exec client npm run lint
```

## Remote

## Odds and Ends

### Fix httpie

In order to get `http` to work in my Windows WSL Ubuntu 20.04 environment, I had to install it with pip and set an alias.

```bash
python3 -m pip install httpie
alias http='python3 -m httpie'
```

### direnv Functions

```bash
lint_backend() {
    echo "Linting Backend Flake8"
    docker-compose exec api flake8 src
    echo "Linting Backend Black"
    docker-compose exec api black src
    echo "Linting Backend Isort"
    docker-compose exec api isort src
}

lint_frontend() {
    echo "Linting Frontend Eslint"
    docker-compose exec client npm run lint
    echo "Linting Frontend Prettier"
    docker-compose exec client npm run prettier:write
}

test_backend() {
    echo "Testing Backtend"
    docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src" --cov-report html
}

test_frontend() {
    echo "Testing Frontend"
    docker-compose exec client npm test
}

project_down() {
    echo "Shutting Project Down"
    docker-compose down -v
}

project_init() {
    project_up
    echo "Setting up test database"
    docker-compose exec api python manage.py recreate_db
    docker-compose exec api python manage.py seed_db
}

project_up() {
    echo "Bringing Project Up"
    docker-compose up -d --build

}

export_function lint_backend
export_function lint_frontend
export_function test_backend
export_function test_frontend
export_function project_down
export_function project_init
export_function project_up
```

## Issues

### Docker: EACCES: permission denied, mkdir '/app/node_modules/.cache'

Need to change folder permissions in the client Dockerfile. Ubuntu mounts volumes with root:root, and we need node:node.

```dockerfile
RUN npm install react-scripts@5.0.1 -g --silent
# Fix EACCES: permission denied
RUN chown -R node:node /usr/src/app/node_modules

# start app
CMD ["npm", "start"]
```

https://stackoverflow.com/questions/67639482/docker-eacces-permission-denied-mkdir-app-node-modules-cache

### Webpack won't rebuild

Windows needs another environment variable to allow auto-rebuild on save.

```yaml
environment:
  - NODE_ENV=development
  - REACT_APP_API_SERVICE_URL=${REACT_APP_API_SERVICE_URL}
  - CHOKIDAR_USEPOLLING=true
  - WATCHPACK_POLLING=true # Fix webpack on windows
```

https://stackoverflow.com/questions/71297042/react-hot-reload-doesnt-work-in-docker-container
