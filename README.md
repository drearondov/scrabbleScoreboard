# Scrabble Scoreboard

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/drearondov/scrabblescoreboard?include_prereleases&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/drearondov/scrabblescoreboard?style=flat-square)

Collect data about Scrabble Games and marvel or cry at the sight of your vocabulary and resourcefulness.

## Endpoints

* `GET /words` - Retrieves a list of all words in dictionary
* `GET /words/languages` - Retrieves a list of all words in a specific language

* `POST /games` - Creates a new game
* `PUT /games` - Edits a game
* `DELETE /games/<int:game_id>` - Deletes a game
* `GET /games/<int:game_id>/plays` - Gets all the plays from a game

* `GET /players` - Gets all players
* `POST /players` - Creates a new player
* `PUT /players/<int:player_id>` - Updates a player based on its id
* `DELETE /players/<int:player_id>` - Deletes a player
* `GET players/<int:player_id>/plays`

* `GET /plays`- Retrieves a list of plays
* `GET /plays/<int: play_id>` - Retrieves info about a play
* `POST /plays` - Creates a new play
* `PUT /plays/<int: play_id>` - Updates a play based on its id
* `DELETE /plays/<int: play_id>` - Deletes a play based on its id

## Resources

* [PostgreSQL](https://www.postgresql.org): Popular and extensible database server.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/): Microframework to create the web application.
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/): Packages used for database management.
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/): Package used for serialization and data validation
* [Flask-restful](https://flask-restful.readthedocs.io/en/latest/): Packages used to create the endpoints
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/): Token based authentication

## Acknowledgements

* [cookiecutter-flask-restful](https://github.com/karec/cookiecutter-flask-restful)  by karec: Cookiecutter used to start the project, a very complete template
