import yaml

from pathlib import Path


DOCSDIR = Path(__file__).resolve().parents[1].joinpath("docs")

yaml_schemas = open(f"{DOCSDIR}/schemas.yml")
schemas = yaml.load(yaml_schemas, Loader=yaml.FullLoader)


swagger_template = {
    "swagger": "3.0",
    "info": {
        "title": "Scrabble Scoreboard",
        "description": "An API to record store data from Scrabble games",
        "version": "0.1.0-beta",
    },
    "components": {
        "schemas": schemas,
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        },
    },
}
