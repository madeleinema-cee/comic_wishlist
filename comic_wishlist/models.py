from comic_wishlist import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Colors(db.Model):
    color_id = db.Column(db.Integer, primary_key=True)
    selected = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    bgcolor = db.Column(db.String(10), nullable=False)
    primary = db.Column(db.String(10), nullable=False)
    secondary = db.Column(db.String(10), nullable=False)
    third = db.Column(db.String(10), nullable=False)
    mute = db.Column(db.String(10), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User('{self.email}')"


