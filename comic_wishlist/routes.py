from flask import render_template
from comic_wishlist import app




@app.route('/')
def index():
    return render_template('home.html')


