from flask import render_template, redirect, url_for, request
from comic_wishlist import app, db
from comic_wishlist.models import Colors, Comics
from comic_wishlist.form import SearchForm


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():
    theme = Colors.query.filter_by(selected=True).first()
    comics = Comics.query.all()
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search', title=form.search_text.data))
    return render_template('home.html', theme=theme, form=form, comics=comics)


@app.route('/home/<int:color_id>')
def select_color(color_id):
    Colors.query.get_or_404(color_id).selected = True
    unchosen_themes = Colors.query.filter(Colors.color_id != color_id).all()
    for unchosen_theme in unchosen_themes:
        unchosen_theme.selected = False
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/search/<string:title>', methods=['GET', 'POST'])
def search(title):
    theme = Colors.query.filter_by(selected=True).first()
    form = SearchForm()
    search_results = Comics.query.filter_by(title=title).order_by(Comics.title.desc())
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search', title=form.search_text.data))
    return render_template('search.html', theme=theme, form=form, search_results=search_results, title=title)