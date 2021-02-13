from scrabbleScoreboard.extensions import db


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    code = db.Column(db.String(2), unique=True)

    words = db.relationship("Word", backref="language", lazy=True)

    def __repr__(self) -> str:
        return f"<Language {self.name}>"

    @classmethod
    def get_by_name(cls, language_name):
        """Queries the database by language name.

        Args:
            language_name (string): Full language name

        Returns:
            Language object: Query result corresponding to selected language.
        """
        return cls.query.filter_by(name=language_name).first_or_404()

    def save(self):
        """Saves current status of language instance."""
        db.session.add(self)
        db.session.commit()
