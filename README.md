
# Term 2 Assignment

I built a web application call **Food Serve Delicious** which let people to host food event to public and meet new friends. After singing up a new account, the user can either host a new event or choose to attend events hosted by other users. A restful API server is hosted as well as the web app runs, other developers can use it to develop their own application.


## Demo Accounts

|Email|Password|
|---|---|
|giraffefrogs@gmail.com|chipswtf|
|apebanana@gmail.com|fishfail|
|monkeychicken@gmail.com|piewth|
|catmince@gmail.com|chickenfail|
|donkeymince@gmail.com|biscuitbrb|
|kangarooegg@gmail.com|broccolilol|
|birdbroccoli@gmail.com|burgerownage|
|trollcarrot@gmail.com|nutswtf|
|octopusice@gmail.com|beefown|
|catpie@gmail.com|chipsownage|


## Directories

```
main.py
|-/templates        // General templates
|-/static           // Static files, such as images
|-/auth             // Authentication blueprint
|-/meal             // Meal blueprint
|-/_lab-work
|-APIs.py           // Restful API server
|-crendentials.py   // Keys and other things which shouldn't be public or put on the repository
|-dump.sql          // Demo data
|-forms.py          // All the forms
|-main.py           // main app
|-models.py         // Models of the data
|-passwordhelper.py // Helper functions for generate hash, salt and validate account.


```

## Achievements:

- [x] Account registration
- [x] Account Login
- [x] Host new food event
- [x] Edit food event
- [x] Delete food event
- [x] Attend food event
- [x] Render food event on google map
- [x] Fetch longitude and latitude of the searched postcode via fetching data from [Postcode API](https://postcodes.io).
- [x] Restful API server.
- [x] Data parser


## Used techniques:

- [x] Flask-login
- [x] Flask-restful
- [x] Flask-blueprint
- [x] Flask-GoogleMaps
- [x] Flask-SQLAlchemy
- [x] Flask-WTF, WTForm
- [x] Postcode API


## Restful API endpoints:

### Users:

#### Date Types

|Key|Type|Description|
|---|----|---|
`id`|Integer| Unique ID of the user
`username`|String| Username of the user
`email`|String| Email of the user
`salt`|String| Salt of the user, it's a random string
`hashed`|String| A hashed for validating users' password
`created_at`|DateTime| The time when the account is created
`authenticated`|Boolean| Whether the account is authenticated.
`activate`|Boolean| Whether the account is activated.
`anonymous`|Boolean| Whether the account is anonymous.


#### Endpoints

|Methods|Route|Description|
|---|---|---|
`GET`|`/api/v1/users`| Get all users' information.
`GET`|`/api/v1/users/<user_id>`| Get an users'information.
`POST`|`/api/v1/users`|Create a new users.
`PUT`|`/api/v1/users/<user_id>`| Update a user's data.
`DELETE`|`/api/v1/users/<user_id>`| Delete a user.

### Meals:

#### Date Types

|Key|Type|Description|
|---|----|---
|`id`|Integer| Unique ID of the meal
|`name`|String| Name of the meal
|`description`|String| A general description of the meal
|`guest_num`|Integer| How many guests could attend this event
|`date`|DateTime| Date of the event
|`time`|DateTime| Time fo the event
|`postcode`|String| The event venue's postcode
|`price`|Float| How much for attending this event
|`lat`|Float| Latitude of the event venue
|`lng`|Float| Longtitude of the event venue
|`user_id`|Integer| The user ID of the host

#### Endpoints

|Methods|Route|Description|
|---|---|---|
`GET`|`/api/v1/meals`| Get all meals' information.
`GET`|`/api/v1/meals/<meal_id>`| Get an meals'information.
`POST`|`/api/v1/meals`|Create a new meals.
`PUT`|`/api/v1/meals/<meal_id>`| Update a meal's data.
`DELETE`|`/api/v1/meals/<meal_id>`| Delete a meal.

### Reservations:

#### Date Types

|Key|Type|Description|
|---|----|---
|`id`|Integer| Unique ID of the reservation
|`meal_id`|Integer| Meal ID of the reservation
|`guest_id`|Integer| User ID of the guest

#### Endpoints

|Methods|Route|Description|
|---|---|---|
`GET`|`/api/v1/reservations`| Get all reservations' information.
`GET`|`/api/v1/reservations/<reservation_id>`| Get an reservations'information.
`POST`|`/api/v1/reservations`|Create a new reservations.
`PUT`|`/api/v1/reservations/<reservation_id>`| Update a reservation's data.
`DELETE`|`/api/v1/reservations/<reservation_id>`| Delete a reservation.

# Lab works

All the lab works are stored in the [subfolder](_lab-work). There are separated folder for each task of all my labs works source codes and the progress records below.

## [Lab 12](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-12)

- [x] Done

## [Lab 13](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-13)

- [x] Task 1: adapting headlines for user input via GET
- [x] Task 2: mocking up a login form using POST
- [x] Task 3: uploading files
- [x] Task 4: flask-wtforms extension
- [x] Task 5: extension task, apply wtforms to file uploads

## [Lab 14](https://github.com/danmcquillan/dnw-flask/wiki/lab-14)

- [x] Task 1: display the twits
- [x] Task 2: adding twits
- [x] Task 3: adding twits using a flask-wtf form
- [x] Task 4: edit and delete twit

## [Lab 15](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-15)

- [x] [Task 1: simple login](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-15#task-1-simple-login)
- [x] [Task 2: restrict access based on logged-in status](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-15#task-2-restrict-access-based-on-logged-in-status)
- [x] [Task 3: use flask-login](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-15#task-3-use-flask-login)
- [x] [Task 4: hashing passwords](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-15#task-4-hashing-passwords)

## [Lab 17](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-17)

- [x] [Task 0: consuming apis](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-17#step-0-consuming-apis)
- [x] [Task 1: creating a simple json api](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-17#step-1-simple-api)
- [x] [Task 2: using flask-restful to create an api](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-17#step-2-using-flask-restful)

## [Lab 18](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-18)

- [x] Task: flask-sqlalchemy

## [Lab 20](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-20)

- [x] [Task 1: twits_blueprint](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-20#step-1-twits_blueprint)
- [x] [Task 2: login_blueprint](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-20#step-2-login_blueprint)
- [x] [Task 3: extension](http://gitlab.doc.gold.ac.uk/data-networks-web/lab-exercises/wikis/lab-20#step-3-extension)
