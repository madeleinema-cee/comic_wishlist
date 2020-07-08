from flask import render_template, redirect, url_for
from comic_wishlist import app, db
from comic_wishlist.models import Colors


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():
    theme = Colors.query.filter_by(selected=True).first()
    return render_template('home.html', theme=theme)


@app.route('/home/<int:color_id>')
def select_color(color_id):
    Colors.query.get_or_404(color_id).selected = True
    unchosen_themes = Colors.query.filter(Colors.color_id != color_id).all()
    for unchosen_theme in unchosen_themes:
        unchosen_theme.selected = False
        db.session.commit()
    return redirect(url_for('index'))

