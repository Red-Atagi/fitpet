# FitPet

## Project Milestone 3B Specifications

### How to Compile
1. Navigate into the `fitpet` directory. You are in the right directory if there is a file `manage.py` (among others) in the directory.
2. You may need to run `pip install django`.
3. Run `python manage.py makemigrations` in the terminal.
4. Run `python manage.py migrate` in the terminal.

*If you have trouble migrating try the command* `python manage.py makemigrations app`

### How to Run the Code
1. Navigate into the `fitpet` directory. You are in the right directory if there is a file `manage.py` (among others) in the directory.
2. Run `python manage.py runserver` in the terminal.
3. You will see a line in your terminal that says: `Starting development server at http://127.0.0.1:8000/`. Note that the port may be different if you already have something running at that port.
4. Go to `http://127.0.0.1:8000/` (or whichever port your terminal says) to see our app.

### How to Run Test Cases
1. Navigate into the `fitpet` directory. You are in the right directory if there is a file `manage.py` (among others) in the directory.
2. Run `python manage.py test app`.

### Acceptance Tests Using Web Interface
1. Register a user using any username, password (at least 8 characters, not too similar to your username), name, and pet's name.
2. Log in with your new account. This should bring you to the home page.
3. From the home page, navigate to the workout page by pressing the button or going to `http://127.0.0.1:8000/workout/`.
4. Log a workout to earn coins.
5. From the home page, navigate to the shop page by pressing the button or going to `http://127.0.0.1:8000/api/buyclothing`.
6. Buy some items with your earned coins.
7. From the home page, navigate to the dress pet page by pressing the button or going to `http://127.0.0.1:8000/dress/`.
8. See your different purchased clothings on your pet.
9. Go back to the home page to see that your pet and its background are updated to what you selected on the dress page.

### Use Cases Implemented
#### Account Creation and Log In
Users can create an account and log in and out of their accounts.

#### Clothing Shop
Users can view the clothing shop, where they can purchase clothing items they do not already have.

#### Dress Pet
Users can try different clothing items on their pets.

#### Workout Plans
Users can log their workout from the given exercises and they will recieve XP for their pet and Coins based on the exercise and reps done.

### Who Did What
- Account Creation: Eric and Gabe
- Clothing Shop: Brandin and Red
- Dress Pet: Alexis and Kaitlyn
- Workout Plans: Josh and Kate

### Changes
The main change we made was switching from using React Native to using Python's Django web framework. This change was made since Django connects the frontend and backend in a way that was easier for our group to understand and create a working product in a short amount of time.

## Tests Location
All of our tests are located in `fitpet/app/tests.py`

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