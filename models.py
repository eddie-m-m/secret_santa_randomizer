from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class SecretSanta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    recipient = db.Column(db.String(25), nullable=True)

    def __init__(self, name, recipient):
        self.name = name
        self.recipient = recipient
