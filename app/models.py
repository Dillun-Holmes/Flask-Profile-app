from . import db


class User(db.Model):
    """User model stores profile information.

    Fields:
        id: primary key
        fullname: user's full name
        email: unique email address
        age: optional integer
        bio: optional biography text
    """
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<User {self.fullname} ({self.email})>"
