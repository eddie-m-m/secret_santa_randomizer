from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class SecretSanta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    santa = db.Column(db.String(25), nullable=False)
    recipient = db.Column(db.String(25), nullable=True)

    def __init__(self, santa, recipient):
        self.santa = santa
        self.recipient = recipient
