from scrabbleScoreboard.extensions import db


class Word(db.Model):
    __tablename__ = "word"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True)
    times_used = db.Column(db.Integer, default=1)

    language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    plays = db.relationship("Play", backref="word", lazy=True)

    def __repr__(self) -> str:
        return f"<Word {self.word}>"

    @classmethod
    def get_by_language(cls, language):
        return cls.query.filter_by(language=language).all()

    @classmethod
    def get_by_word(cls, word):
        return cls.query.filter_by(word=word).first_or_404()

    def update_word_count(self):
        self.times_used += 1

    def save(self):
        db.session.add(self)
        db.session.commit()
