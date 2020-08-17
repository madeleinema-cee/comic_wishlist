from flask import render_template, redirect, url_for, request
from comic_wishlist import app, db
from comic_wishlist.models import Colors
from comic_wishlist.form import SearchForm
from find_data import ComicData
from download_data import ExcelCovert


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    theme = Colors.query.filter_by(selected=True).first()
    comics = ComicData(wishlist=True)
    comics = comics.parse_data()

    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search_wishlist', title=form.search_text.data))
    return render_template('home.html', theme=theme, form=form, comics=comics)


@app.route('/collection', methods=['GET', 'POST'])
def find_collection():
    theme = Colors.query.filter_by(selected=True).first()
    comics = ComicData(wishlist=False)
    comics = comics.parse_data()

    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search_collection', title=form.search_text.data))
    return render_template('collection.html', theme=theme, form=form, comics=comics)


@app.route('/search_wishlist/<string:title>', methods=['GET', 'POST'])
def search_wishlist(title):
    titles = []
    theme = Colors.query.filter_by(selected=True).first()
    titles.append(title.lower())
    comics = ComicData(wishlist=True)
    comics = comics.parse_data()

    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search_wishlist', title=form.search_text.data))
    return render_template('home.html', theme=theme, form=form, comics=comics, titles=titles)


@app.route('/collection/<string:title>', methods=['GET', 'POST'])
def search_collection(title):
    titles = []
    theme = Colors.query.filter_by(selected=True).first()
    titles.append(title.lower())
    comics = ComicData(wishlist=False)
    comics = comics.parse_data()

    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            return redirect(url_for('search_collection', title=form.search_text.data))
    return render_template('collection.html', theme=theme, form=form, comics=comics, titles=titles)


@app.route('/home/<int:color_id>')
def select_color(color_id):
    Colors.query.get_or_404(color_id).selected = True
    unchosen_themes = Colors.query.filter(Colors.color_id != color_id).all()
    for unchosen_theme in unchosen_themes:
        unchosen_theme.selected = False
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/utilities')
def utilities():
    theme = Colors.query.filter_by(selected=True).first()

    return render_template('utilities.html', theme=theme)


@app.route('/utilities/<wishlist>/<one_sheet>')
def download_excel(wishlist, one_sheet):
    e = ExcelCovert(wishlist=wishlist, one_sheet=one_sheet)
    if one_sheet == 'True':
        e.download_one_sheet()
    else:
        e.download_multi_sheet()
    return redirect(url_for('index'))

