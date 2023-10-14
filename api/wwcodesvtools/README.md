# WWCode-SV Chapter Tools API

- REST API using [Django REST Framework](https://www.django-rest-framework.org/).

Clone the [WWCode-SV](https://github.com/WomenWhoCode/WWCode-SV) repository to your local machine.

The Backend working directory is [WWCode-SV/api/wwcodesvtools/](https://github.com/WomenWhoCode/WWCode-SV/tree/master/api/wwcodesvtools).

## Requirements
- Git
- [Docker Community Edition](https://docs.docker.com/install/)
- An Integrated Development Environment (IDE) like [VSCode](https://code.visualstudio.com/)


## Setup instructions using Docker:
There are two main files in the project used to setup the application in order to use Docker:
- Dockerfile.dev: It is a Dockerfile that contains all the commands needed to build a Docker image. The image contains all the dependencies the application requires.
- docker-compose.yml: It defines the services(web, db and migrations) that make up the application, so they can be run together in an isolated environment. It includes a reference to the Dockerfile.dev file.

Docker will create a container for each service defined in the [docker-compose.yml](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/docker-compose.yml) file.

The following instructions will allow you to run the application using Docker.


1. Install [Docker Community Edition](https://docs.docker.com/install/) if it is not already installed.
2. In the terminal, navigate to the Backend directory:
    ```
     $ cd api/wwcodesvtools/
    ```
3. Create your own copy of the enviroment variables file:
    ```
    $ cp .env.example .env
    ```
4. Before you bring up the Docker containers for the first time or rebuild them, comment out [ApiConfig.ready()](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/api/apps.py) function in the `apps.py` file to prevent flush token error.
5. Once Docker is installed, create/start the container in order to run the application:
    ```
    $ docker-compose up
    ```

   Docker creates a container for the project with three services: web, migrations and db.

6. The web application will be available at http://localhost:8000.

   In order to see the list of the existing API endpoints go to: http://localhost:8000/swagger.

**NOTE:** After running the application, revert back step 4. Uncomment the [ApiConfig.ready()](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/api/apps.py) function in the `apps.py` file.

### Compose
Generally it is more convenient to run the containers in the background using daemon mode. To start the containers in daemon mode, use the following command:
```
$ docker-compose up -d
```
To check if the containers are running, use:
```
$ docker-compose ps
```
To rebuild all the containers, use the following command:
```
$ docker-compose up -d --build
```
To restart the web service, run:
```
$ docker-compose restart web
```
To run any command in the app container, use:
```
$ docker-compose exec web <command>
```

To be able to interactively run or debug inside the container environment, run:
```
$ docker-compose exec <service> bash
```

For example:
```
$ docker-compose exec web bash
```

### Logs
To tail logs, run:
```
$ docker-compose logs -f web
```

### Migrations
When you bring up docker containers for the first time or rebuild them,
migrations are automatically run. If your containers are already running and
you want to add a few migrations and run migrations in the db, you can use the
following commands.

To make a new migration, run:
```
$ docker-compose exec web python manage.py makemigrations --name <name of migration>
```
To run migrations, run:
```
$ docker-compose exec web python manage.py migrate --noinput
```

### Shut down
To stop the containers but not remove them, run:
```
$ docker-compose stop
```

To stop and remove containers, run:
```
$ docker-compose down
```

To stop and remove all containers, as well as volumes as networks, run:
```
$ docker-compose down -v
```
This command is helpful if you want to start with a clean slate. However, it
will completely remove any data you have already stored in the database.


### How to create first few intial users in the local database
* Run below command
```
$ docker-compose exec web bash ./manage.py loaddata api/fixtures/users_data.json
```

This will create the below users in the local db with 'Password123'
```
            user_name            | first_name | last_name
---------------------------------+------------+-----------
 director@example.com            | John       | Smith
 volunteer@example.com           | Alice      | Robinson
 leader@example.com              | Bruno      | Clark
 leaderPendingStatus@example.com | Caroline   | Miller
 brendajackson@example.com       | Brenda     | Jackson
 sophiefisher@example.com        | Sophie     | Fisher
 alexanderbrown@example.com      | Alexander  | Brown
 jackross@example.com            | Jack       | Ross
 sophiebutler@example.com        | Sophie     | Butler
```


Here are the users details with roles and teams:
```
 user_id |            user_name            |    FN     |    LN    | role_name | status  |       team_name
---------+---------------------------------+-----------+----------+-----------+---------+------------------------
       1 | director@example.com            | John      | Smith    | DIRECTOR  | ACTIVE  | Social Media Team
       2 | volunteer@example.com           | Alice     | Robinson | VOLUNTEER | ACTIVE  | Partnership Management
       2 | volunteer@example.com           | Alice     | Robinson | VOLUNTEER | ACTIVE  | Social Media Team
       2 | volunteer@example.com           | Alice     | Robinson | VOLUNTEER | ACTIVE  | Host Management
       3 | leader@example.com              | Bruno     | Clark    | LEADER    | ACTIVE  | Event Volunteers
       3 | leader@example.com              | Bruno     | Clark    | LEADER    | ACTIVE  | Volunteer Management
       4 | leaderPendingStatus@example.com | Caroline  | Miller   | LEADER    | PENDING |
       5 | brendajackson@example.com       | Brenda    | Jackson  | DIRECTOR  | ACTIVE  |
       6 | sophiefisher@example.com        | Sophie    | Fisher   | VOLUNTEER | ACTIVE  | Hackathon Volunteers
       6 | sophiefisher@example.com        | Sophie    | Fisher   | LEADER    | ACTIVE  | Tech Event Team
       7 | alexanderbrown@example.com      | Alexander | Brown    | LEADER    | ACTIVE  |
       8 | jackross@example.com            | Jack      | Ross     | LEADER    | PENDING |
       9 | sophiebutler@example.com        | Sophie    | Butler   | DIRECTOR  | ACTIVE  | Partnership Management
       9 | sophiebutler@example.com        | Sophie    | Butler   | LEADER    | ACTIVE  | Event Volunteers
```

## How to use test APIs using swagger
* Go to /swagger/ to access the API documentation.

For endpoints that need authentication and authorization,
* Click on Django Login button:
    - Login using the username and password.

        Some endpoints are restricted to the director role, so it is recommended to login with a user with this role in order to have access to all endpoints.
    - Copy the "access" token: the alphanumeric value that is between double quotes (" ").

<img width="1187" alt="Screen Shot 2023-05-10 at 5 24 58 PM" src="https://github.com/WomenWhoCode/WWCode-SV/assets/102187795/f596a659-f150-4758-a9d2-f71d84e68a70">


Go back to /swagger/

* Click on Authorize button:
    - In the Value text box, enter "Bearer", leave a space and paste the value of the access $token$.
      This will add an authorization key which will have the "Bearer $token$" as the value in the request header.


<img width="642" alt="Screen Shot 2023-05-10 at 5 25 39 PM" src="https://github.com/WomenWhoCode/WWCode-SV/assets/102187795/5f34a048-f6b9-4a83-95cf-6b993a460c9f">


**NOTE:** Do not include the double quotes (" ") either when copying the access token or when entering the values in the text box.


You will be authorized at this point. You will see the lock icons closed as an indicator.

* Click on each endpoint and click on "Try it out" to send requests to the API.


## How to contribute

* Please follow the following naming convention for branch:

    BE-SprintXFeatureNameIssue#Developer

    E.g.: BE-Sprint1UserLogin#12Rita

    * Feature name can be shortened so that it’s not too long

Refer to the [Technical Guide for Backend](https://github.com/WomenWhoCode/WWCode-SV/wiki/Technical-Guide-for-Backend) for guidelines and other useful information.

## How to enable swagger and redoc documentation for your API

Swagger and redoc documentation for the APIs can be automatically generated by ensuring
some simple steps in your views.
* Make sure that your view class has a `serializer_class` variable defined and is pointing
to the serializer class that the view uses.
* Swagger does not do a good job in automatically documenting the responses. To document the
response of the API properly, define a dictionary that can contain the openapi schema for the
responses. The schema has all the possible responses from the API along with a brief description
and examples.
Example:
```
post_response_schema = {
        status.HTTP_201_CREATED: openapi.Response(
            description="User successfully created",
            examples={
                "application/json": {}
            }
        ),
        ERROR_STATUS[EXPECTED_KEY_NOT_PRESENT_IN_REQUEST]: openapi.Response(
            description="Key error: Key not present",
            examples={
                "application/json": {
                    "error": EXPECTED_KEY_NOT_PRESENT_IN_REQUEST.format("email not present")
                }
            }
        ),
    }
```
* Use the @swagger_auto_schema decorator to override the swagger auto schema generation
for the responses.
Example:
```
@swagger_auto_schema(responses=post_response_schema)
def post(self, request):
    ...
```
* To check out the documentation, open `/redoc/` or `/swagger/`

## Deploying the Backend API on [Railway](railway.app)
The following instructions are specific to deploy the backend application on Railway, assuming the initial project setup on Railway is done.

* [Install Railway CLI](https://docs.railway.app/develop/cli) following the instructions for your operating system.

For deploying the application on Railway, we use the dockerfile [`Dockerfile`](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/Dockerfile). It contains the commands to be run while deploying, to install all the dependencies and execute the Django related commands to run migrations, collect static files and load fixtures(in dev only).


1. Open the [`Dockerfile`](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/Dockerfile) and comment out/uncomment the following lines depending on the environment you are deploying:

* Development Environment:
    ```
    CMD  python manage.py migrate && python manage.py loaddata api/fixtures/users_data.json && python manage.py collectstatic --noinput && gunicorn wwcodesvtools.wsgi:application --bind 0.0.0.0:$PORT
    ```
* Staging Environment:
    ```
    CMD  python manage.py migrate && python manage.py collectstatic --noinput && gunicorn wwcodesvtools.wsgi:application --bind 0.0.0.0:$PORT
    ```


**NOTE:**  The difference between these two commands is `loaddata`. We don't need to load fixtures in the stage environment.

 Before continue, check that the containers are working on the localhost.

2. Using your terminal, login to your Railway account:
    ```
    railway login
    ```
    It opens a browser tab which authenticates your Railway account.
    For deploying the Chapter Tools API, you will need the credentials for the WWCode account. Ask the leaders for details.

3. Navigate to the [backend project directory](https://github.com/WomenWhoCode/WWCode-SV/tree/master/api/wwcodesvtools), where the Dockerfile is, and link it to the Railway project you intent to deploy (Development or Stage):

    ```
    railway link [projectId]
    ```
    Running ```link``` with no project ID will prompt you to select an existing project from the WWCode Railway account.

    * Development Env Project: **wwcode-chtools-api-dev**

    * Stage Env Project: **wwcode-chtools-api-stage**

    You can find the ProjectId on Railway(web), selecting the project then under the Settings > General > Project Info page.


4.  Deploy the previously linked project directory:

    ```
    railway up
    ```

    Make sure you are in the backend directory (where the Dockerfile is) because if no path is provided the current directory is deployed.


If there is no errors during the deployment process, you will be able to access the application.

   * Dev environment:   https://wwcode-chtools-api-dev-development.up.railway.app/swagger/
   * Staging environment: https://wwcode-chtools-api-stage-production.up.railway.app/swagger/

During the deployment process, Railway generates build logs and deploy logs. In case an error occurs, you can review what happened in the process.

## Other Railway commands
* View logs for the most recent deployment.
    ```
    railway logs
    ```
* Open an interactive shell to a database directly in the CLI.
    ```
    railway connect
    ```
* View the status of your Railway project and user.
    ```
    railway status
    ```
* Logout of your Railway account.
    ```
    railway logout
    ```
* Open your current Railway project in the browser.
    ```
    railway open
    ```
* Disconnects the current directory from Railway. You will need to rerun railway init to use railway in this directory again.
    ```
    railway unlink
    ```

For more commands available in Railway CLI:
https://docs.railway.app/reference/cli-api


## Deploying onto Heroku (Deprecated)
* Check that the containers are working on the localhost.
* Comment out [ApiConfig.ready()](https://github.com/WomenWhoCode/WWCode-SV/blob/master/api/wwcodesvtools/api/apps.py) function prior to deploy to prevent flush token error
```
Comment out  ApiConfig.ready() in the apps.py file
```
* Login to heroku
```
heroku login
```

* Login for heroku container registry
```
heroku container:login
```

* Build and push container to heroku registry
```
heroku container:push web -a wwcode-chtools-api -r <git remote of app>

heroku container:push web -a wwcode-chtools-api -r wwcode-chtools-api
```

* Release container on heroku
```
heroku container:release web -a wwcode-chtools-api -r <git remote of app>

heroku container:release web -a wwcode-chtools-api -r wwcode-chtools-api
```

* Check releases
```
heroku releases -a wwcode-chtools-api
```

* Check logs
```
heroku logs --tail -a wwcode-chtools-api
```

* To set a config for secret_key or anything else
```
heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a wwcode-chtools-api
```
The config variables set in this way are available as environment variables to
the application.

* Check environment variables that are available to the app
```
heroku run env -a wwcode-chtools-api
```

* SSH into the dyno
```
heroku ps:exec --dyno=web.1 -a wwcode-chtools-api
```
Environment variables cannot be accessed by ssh-ing in the dyno.

* Run migrations in the app
```
heroku run python manage.py migrate --noinput -a wwcode-chtools-api
```


