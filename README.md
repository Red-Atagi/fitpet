# FitPet

## File Structure
```
data_241_autumn_2024_1/
├── README.md
└── fitpet/
    ├── app
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── base.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── db.sqlite3
    ├── fitpet
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py
```

## Virtual Environment (for Mac)

1. Make a virtual environment in the base directory called `env` by typing `python -m venv .env`
2. Activate the virtual environment by typing `source .env/bin/activate`.

## Working on the project

The bulk of the project will be worked on in the `fitpet/app` directory.

The `templates` directory holds all the html files for the UI.

`urls.py` define which function in `views.py` are called when there is a HTTP request from that url.

`views.py` takes in HTTP requests and return a web response. It requests/sends data to `models.py`.

`models.py` defines the classes and holds most of the logic of the app.

## Running the Webserver

1. If the class structure has changed, then the database structure will also change. Thus, you need to run `python manage.py makemigrations` then `python manage.py migrate`.
2. To run the webserver, run `python manage.py runserver`.