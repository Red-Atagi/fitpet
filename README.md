# FitPet

## Project Milestone 5

### Project Purpose
This project aims to build a web app for users to log their workouts and use their rewards to dress their virtual pet. Users can add their friends and see their friends' pets as well.

### How to Compile
1. Navigate into the `fitpet` directory. You are in the right directory if there is a file `manage.py` (among others) in the directory.
2. You may need to run `pip install django`.
3. Run `python manage.py makemigrations` in the terminal.
	-  make sure you're in fitpet/ directory
4. Run `python manage.py migrate` in the terminal.

*If you have trouble migrating try the command* `python manage.py makemigrations app`.

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
5. From the home page, navigate to the shop page by pressing the button or going to `http://127.0.0.1:8000/shop`.
6. Buy some items with your earned coins.
7. From the home page, navigate to the dress pet page by pressing the button or going to `http://127.0.0.1:8000/dress/`.
8. See your different purchased clothings on your pet.
9. Go back to the home page to see that your pet and its background are updated to what you selected on the dress page.
10. Register another user using any username, password (at least 8 characters, not too similar to your username), name, and pet's name.
11. Log in to the new account. This should bring you to the home page.
12. From the home page navigate to the friends list page by clicking on "friends" or going to `http://127.0.0.1:8000/friends/list/`
13. You'll see that you don't have any friends
14. From the friend list page navigate to the find friends page by clicking "find new friends" or going to `http://127.0.0.1:8000/search_users/`
15. Search the username of the first account and click "Send Request" to send a friend request
16. Log out and Log in to the user you sent the friend request to 
17. From the friends list page navigate to the check friend request by clicking "Check Friend Request" or going to `http://127.0.0.1:8000/friends/list/`
18. You should see the friend request you just sent. Click accept friend request and then return to friends list. You'll see your new friend in you friends list
19. Click "visit {name}" and see the profile of your new friend
20. You can change users and dress the pet in new clothing, purchase new items, log more exercises and level up and it will change in the friends profile 

## Project Milestone 4B
### Usecases Implemented In Iteration 2
#### Send Friend Request
A user can search for other users by their username through the find new friends page and send them a friend request

#### Check Friend Request
A user can check their friend requests and accept or decline users who have sent a friend request

#### Vist Friends
A user can see a list of their friends and click visit to see their friends stats, pet, owned clothed, and their other friends

### Who did What
- Send Friend Request: Eric and Gabe
- Visit Friends and clothing drawings: Brandin and Red
- Website Design Alexis and Kaitlyn
- Chekc Friend Request: Josh and Kate

### Changed and Not changed
We were able to implement most of the use cases for the user: create account, log in, workout, shop, dress pet, send friend request, check friend request (accept and decline friend request), visit friend. We only have one pet design so we did not implement choose pet use case create account. We didn't implmenent the administrator use cases: add exercises, delete exercises. However we can edit a file /fitpet/app/data/exercise.json to add new exercises.

### Acceptance Test
1. Register at least two users using any username, password (at least 8 characters, not too similar to your username), name, and pet's name.
2. Log in to one of the new account. This should bring you to the home page.
2. From the home page navigate to the friends list page by clicking on "friends" or going to `http://127.0.0.1:8000/friends/list/`
3. You'll see that you don't have any friends
3. From the friend list page navigate to the find friends page by clicking "find new friends" or going to `http://127.0.0.1:8000/search_users/`
4. Search the username of the account you just logged out of and click "Send Request" to send a friend request
5. Log out and Log in to the user you sent the friend request to 
6. From the friends list page navigate to the check friend request by clicking "Check Friend Request" or going to `http://127.0.0.1:8000/friends/list/`
7. You should see the friend request you just sent. Click accept friend request and then return to friends list. You'll see your new friend in you friends list
8. Click "visit {name}" and see the profile of your new friend
9. You can change users and dress the pet in new clothing, purchase new items, log more exercises and level up and it will change in the friends profile 

## Project Milestone 4A

### 2nd Iteration Plan

We plan to finish the use cases for the users which includes visit friend, check friend requests, send friend requests, and work on the design and cohesiveness of our html page. We’re not implementing the administrator side of the application which includes add exercise and delete exercise.

### Who will work on what

#### visit friend: Red and Brandin
- view friend list page
- display the friend’s pet, background, and clothing
#### check friend requests: Kate and Josh
- check friend requests from friend list page
- see pending requests (name and username of other user)
- accept or decline friend request
#### send friend request: Gabe and Eric
- accessed thru button on friend list page
- search for other users
#### design: Kaitlyn and Lexi
- redesing the website to add cohesiveness

### Unit Tests for Iteration 2
Our unit tests for iteration 2 are loacted in fitpet/app/tests-2.py. You can run all tests including iteration 1 with the command `python manage.py test app` if you want to run just iterations 2 tests you can run `python manage.py test app.tests-2`

## Project Milestone 3B Specifications

### How to Compile
1. Navigate into the `fitpet` directory. You are in the right directory if there is a file `manage.py` (among others) in the directory.
2. You may need to run `pip install django`.
3. Run `python manage.py makemigrations` in the terminal.
	-  make sure you're in fitpet/ directory
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
5. From the home page, navigate to the shop page by pressing the button or going to `http://127.0.0.1:8000/shop`.
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
    |   ├── tests-2.py
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