
# flixfinder-backend

Backend for flixfinder app written using Python 3 and Django 2.

## Usage

_These instructions assume you're using Linux, they should be easy to adapt to other platforms._

Check it out
```
git clone https://github.com/AmalgamProjects/flixfinder-backend.git
cd flixfinder-backend
```

Setup python virtual environment
```
python3.7 -m venv env
. ./env/bin/activate
pip install --upgrade pip wheel
```

Install required dependencies and the run development server
```
cd src/
pip install -r requirements.txt
./manage.py runserver
```

### Database

Your local instance will be using `SQLite 3` by default. To connect to a `MySql` instance you will need to override `flixfinder/settings.py`. See the Django documentation for the `DJANGO_SETTINGS_MODULE` variable for more details.
 - https://docs.djangoproject.com/en/2.2/topics/settings/

To connect to the cloud instance of the `flixfinder-develop` database you should use the `Google Cloud SQL Proxy`. Detailed instructions are in the Google Cloud documentation/
 - https://cloud.google.com/sql/docs/mysql/sql-proxy
 - https://cloud.google.com/sql/docs/mysql/quickstart-proxy-test

Note that your database will start out empty as we do not keep demo data in this repo.

## Production Usage

We run this project on Google App Engine Standard Environment.
 - https://cloud.google.com/appengine
 - https://cloud.google.com/appengine/docs/python

We use GitHub Actions to automatically deploy changes.
 - https://github.com/features/actions

Please see the `flixfinder-deploy` repository for further details.
 - https://github.com/AmalgamProjects/flixfinder-deploy

## Structure

This project has two applications.

`ff_api` contains the REST API.

`ff_spa` contains the server side necessary for serving the frontend.


