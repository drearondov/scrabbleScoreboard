from scrabbleScoreboard.extensions import db

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(60), unique=True)

    words = db.relationship('Word', backref='language', lazy=True)

    def __repr__(self) -> str:
        return f'<Language {self.language}>'

    @classmethod
    def get_by_language(cls, language):
        return cls.query.filter_by(language=language).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
