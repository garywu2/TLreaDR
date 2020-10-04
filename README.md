# TLreaDR

[![Build Status](https://travis-ci.org/YaleDHLab/flask-react-boilerplate.svg?branch=master)](https://travis-ci.org/YaleDHLab/flask-react-boilerplate)

TLreaDR is a React + Flask application which allows users to summarize news articles into "easy to read" posts with other's through liking, disliking and commenting on content.

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

4. Copy paste the .env file into each of the microservices directories so that they can have access to the database.

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

### Development

To run both the server and client, you can run the following command:

```bash
npm run dev
```

This will run the the client on 7081 and the server's microservices will run on:

* Server service: 7082
* User service: 7083
* Post service: 7084
* Comment service: 7085
* Command service: 7086

### Production
To run all services including the front-end as a docker container 
uncomment the front-end service from the docker-compose.yml and run the following
```bash
docker-compose up --build
```
