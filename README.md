# Scrabble Scoreboard

Collect data about Scrabble Games and marvel or cry at the sight of your vocabulary and resourcefulness.

## Technologies used

* SQLite3 for a small portable database.
* Flask to create the web application and later serialize it.
* Flask-SQLAlchemy and Flask-Migrate for database management.

## Endpoints

* `GET /words` - Retrieves a list of all words in dictionary
* `GET /words/languages` - Retrieves a list of all words in a specific language

* `POST /games` - Creates a new game
* `PUT /games` - Edits a game
* `DELETE /games/<int:game_id>` - Deletes a game
* `GET /games/<int:game_id>/plays` - Gets all the plays from a game

* `POST /players` - Creates a new player
* `PUT /players/<int:player_id>` - Updates a player based on its id
* `DELETE /players/<int:player_id>` - Deletes a player
* `GET players/<int:player_id>/plays`

* `GET /plays`- Retrieves a list of plays
* `GET /plays/<int: play_id>` - Retrieves info about a play
* `POST /plays` - Creates a new play
* `PUT /plays/<int: play_id>` - Updates a play based on its id
* `DELETE /plays/<int: play_id>` - Deletes a play based on its id
