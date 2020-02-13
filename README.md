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

## Quickstart

To run both the server and client, you can run the following command:

```bash
npm run dev
```

This will run the server on port 5000 (defaulted by debug mode) and the client on 7081

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