# PlanetlyTask

## Walkthrough

PlanetlyTask is a RESTful APIs built upon Django Rest Framework using Django ORM and PostgreSql. The service is built inside a Docker container and can leverage `docker-compose`. It exposes CRUD functionality to a database that stores carbon usage trend for customers. It also supports pagination, sorting and filtering based on time range. It took me around 6 hours spanned across 3 days to complete the challenge.

## Local Setup

* You need Python 3+ and Docker to run this application.
* Clone this repo and go to the cloned repo 
* Create a `.env` file inside `PlanetlyTask/carbonusage`. Here you will find `.env.example`. Please follow this file to create environment variables.
*  Execute below commands
	* `docker compose up --build` : It will build the containers
	* `docker compose exec carbonusage python3 manage.py migrate --noinput`  : It will migrate all the necessary models

> **PS:** I have developed this application on Mac, thus the docker commands may vary for different OS.

## API Endpoints

* API documentation is available on `localhost:8000` and can be accessed through Swagger.

## Features

* User can register/login to the application through Token Authentication.
* Fully functioning CRUD operations on User and Carbon Usage models.
* API has ability to handle pagination, sorting and filtering.
* API also provides carbon usage details for selected user.
* Unit Test Cases are available for major end points. You can run them through `python3 manage.py test`
* API documentation is available on `localhost:8000` and can be accessed through Swagger.

## Challenges
* Writing test cases for modules that is behind the token authentication.
* Handling filter and sorting in API  from django_filters.


## Area of improvements

* Currently API `api/v1/users/<pk>` does not support multi delete functionality. User can only delete single record at a time.
* Pagination allows 2 records per page but we can modify the api `api/v1/usages/` so that it can be customisable through frontend. 
* Usage API currently has single fetch functionality which seems redundant current scope. But we can utilise it to show the details on the frontend.