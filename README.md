# Scrabble Counter

I build this project to help me collect data from the Scrabble games we play at home, and either marvel or cry at the sight of our own vocabulary and resourcefulness.

## Technologies used

* SQLite3 for a small portable database.
* Flask to create the web application and later serialise it.
* Flaks-SQLAlchemy and Flask-Migrate for database management.

## Endpoints

* `GET /words` - Retrieves a list of all words in dictionary
* `GET /plays`- Retrieves a list of plays

* `POST /plays` - Creates a new play
* `POST /players` - Creates a new player
* `POST /game` - Creates a new game

* `PUT /plays/:id` - Updates a play based on its id
* `PUT /players/:id` - Updates a player based on its id

* `PATCH /plays/:id` - Partially updates a play

* `DELETE /plays/:id` - Deletes a play
* `DELETE /player/:id` - Deletes a player
* `DELETE /game/:id` - Deletes a game
