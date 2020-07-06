from comic_wishlist import db


class Color(db.Model):
    color_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    bgcolor = db.Column(db.String(10), nullable=False)
    primary = db.Column(db.String(10), nullable=False)
    secondary = db.Column(db.String(10), nullable=False)
    third = db.Column(db.String(10), nullable=False)
    mute = db.Column(db.String(10), nullable=False)
