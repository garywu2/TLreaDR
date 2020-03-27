# Flask React Boilerplate

[![Build Status](https://travis-ci.org/YaleDHLab/flask-react-boilerplate.svg?branch=master)](https://travis-ci.org/YaleDHLab/flask-react-boilerplate)

Simple boilerplate for a Flask backend and React client including:

* ES6 transpiling via Webpack
* Hot module reloading via Webpack Dev Server
* State management via Redux
* Tests via Pytest and Jest
* Linting via Pylint and Eslint
* Travis CI for automatic testing and linting

## Dependencies

To install the boilerplate dependencies, you can run:

```bash
git clone https://github.com/YaleDHLab/flask-react-boilerplate
cd flask-react-boilerplate
npm install --no-optional
pip install -r requirements.txt
```

Additionally, you need a .env file to store the private credentials used to connect to the database.

To do this follow these steps:

1. Create a **.env** file in the root project directory
2. Generate a SECRET_KEY using the python shell

```
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
```

3. Add the following lines into the .env file

```
SECRET_KEY='the secret key you generated in step 2'
SQLALCHEMY_DATABASE_URI='postgresql://{username}:{password}@{JDBC_URL}/postgres
```

### Configuring Docker Microservices

*  Download docker for your platform and check if it is correctly installed using:

```
docker --version
``` 

* Build docker containers

```
docker-compose up --build
```

## Quickstart

To run both the server and client, you can run the following command:

```bash
npm run dev
```

This will run the the client on 7081 and the server's microservices will run on:

* User service: 7082
* Post service: 7083
* Comment service: 7084

## Tests

To run the Javascript tests (located in `src/tests/`), run:

```bash
npm run jest
```

To run the Python tests (located in `server/tests/`), run:

```bash
pytest
```

## Linting

To lint the Javascript files (located in `src`), run:

```bash
npm run lint-js
```

To lint the Python files (located in `server`), run:

```bash
npm run lint-py
```
