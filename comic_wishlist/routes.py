from flask import render_template
from comic_wishlist import app
from comic_wishlist.models import Color


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():
    color_choice = Color.query.filter_by(name='ironman').first()
    return render_template('home.html', color_choice=color_choice)


