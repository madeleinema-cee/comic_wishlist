from comic_wishlist import db


class Colors(db.Model):
    color_id = db.Column(db.Integer, primary_key=True)
    selected = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    bgcolor = db.Column(db.String(10), nullable=False)
    primary = db.Column(db.String(10), nullable=False)
    secondary = db.Column(db.String(10), nullable=False)
    third = db.Column(db.String(10), nullable=False)
    mute = db.Column(db.String(10), nullable=False)


class Presses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comics = db.relationship('Comics', backref='comic', lazy=True)

class Comics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    issues = db.relationship('Issues', backref='name', lazy=True)
    press = db. Column(db.Integer, db.ForeignKey('presses.id'), nullable=False)



class Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_title = db.Column(db.String(100), nullable=True)
    number = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'), nullable=False)