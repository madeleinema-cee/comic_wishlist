from flask import render_template, redirect, url_for, request, send_file
from comic_wishlist import app, db
from comic_wishlist.models import Colors
from comic_wishlist.form import SearchForm, AdvancedForm1, AdvancedForm2
from find_data import ComicData
from download_data import ExcelCovert
from datetime import datetime as dt
from utils import retrieve_oldest_comic_date, generate_date_options



@app.route('/', methods=['GET', 'POST'])
def index():
    theme = Colors.query.filter_by(selected=True).first()
    comics = ComicData(wishlist=True, query=None)
    comics = comics.parse_data(wishlist=True)

    advanced_form = AdvancedForm1()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_wishlist', title=search_form.search_text.data))

        elif advanced_form.submit2.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_wishlist', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data))
    return render_template('home.html', theme=theme, search_form=search_form, advanced_form=advanced_form, comics=comics,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/advanced_search_wishlist/<string:title>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def advanced_search_wishlist(title, start_date, end_date):
    theme = Colors.query.filter_by(selected=True).first()

    query = f'''
                    select p.PublisherName, c.title, c.covertitleid, c.description, i.issuenumber, i.issueid,
                    i.coverdate, i.covervariantdescription from WishList w
                    join Issue i on  w.issueid = i.IssueId
                    Join CoverTitle c on i.covertitleid = c.covertitleid
                    join Publisher p on p.publisherid = c.publisherid
                    where coverdate between '{start_date}-01-01' and '{end_date}-12-31'
                    and title like '%{title}%'
                    Order by PublisherName, title, issuenumber'''
    title = [title.lower()]
    results = ComicData(wishlist=True, query=query)
    results = results.parse_data(wishlist=True)

    comics = ComicData(wishlist=True, query=None)
    comics = comics.parse_data(wishlist=True)

    advanced_form = AdvancedForm1()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_wishlist', title=search_form.search_text.data))

        elif advanced_form.submit2.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_wishlist', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data))
    return render_template('home.html', theme=theme, search_form=search_form, advanced_form=advanced_form,
                           comics=comics, start_date=start_date, end_date=end_date, results=results, title=title,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/search_wishlist/<string:title>', methods=['GET', 'POST'])
def search_wishlist(title):
    titles = []
    theme = Colors.query.filter_by(selected=True).first()
    titles.append(title.lower())
    comics = ComicData(wishlist=True)
    comics = comics.parse_data(wishlist=True)

    advanced_form = AdvancedForm1()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_wishlist', title=search_form.search_text.data))

        elif advanced_form.submit2.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_wishlist', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data))

    return render_template('home.html', theme=theme, search_form=search_form, advanced_form=advanced_form,
                           comics=comics, titles=titles, year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/collection', methods=['GET', 'POST'])
def find_collection():
    theme = Colors.query.filter_by(selected=True).first()
    comics = ComicData(wishlist=False)
    comics = comics.parse_data(wishlist=False)
    advanced_form = AdvancedForm2()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_collection', title=search_form.search_text.data))

        elif advanced_form.submit3.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_collection', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data, graded=advanced_form.graded.data))
    return render_template('collection.html', theme=theme, search_form=search_form,
                           advanced_form=advanced_form, comics=comics,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/collection/<string:publisher>', methods=['GET', 'POST'])
def find_one_collection(publisher):
    theme = Colors.query.filter_by(selected=True).first()
    publisher = publisher.replace('%20', ' ')
    query = f'''
               select p.PublisherName, c.title, c.covertitleid, c.description, i.issuenumber, i.issueid,
                i.coverdate, i.covervariantdescription, u.cgccolor, u.cgcscore, u.cgccomments from Issue i
               join UserIssue u on u.issueid = i.issueid
               Join CoverTitle c on i.covertitleid = c.covertitleid
               join Publisher p on p.publisherid = c.publisherid
               where publishername is '{publisher}'
               Order by PublisherName, title, issuenumber'''

    comics = ComicData(wishlist=False, query=query)
    comics = comics.parse_data(wishlist=False)
    advanced_form = AdvancedForm2()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_collection', title=search_form.search_text.data))

        elif advanced_form.submit3.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_collection', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data, graded=advanced_form.graded.data))
    return render_template('find_one_collection.html', publisher=publisher, theme=theme, search_form=search_form,
                           advanced_form=advanced_form, comics=comics,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/advanced_search_collection/<string:title>/<string:start_date>/<string:end_date>/<graded>', methods=['GET', 'POST'])
def advanced_search_collection(title, start_date, end_date, graded):
    theme = Colors.query.filter_by(selected=True).first()

    query = f'''
            select p.PublisherName, c.title, c.covertitleid, c.description, i.issuenumber, i.issueid,
             i.coverdate, i.covervariantdescription, u.cgccolor, u.cgcscore, u.cgccomments from Issue i
            join UserIssue u on u.issueid = i.issueid
            Join CoverTitle c on i.covertitleid = c.covertitleid
            join Publisher p on p.publisherid = c.publisherid
            where coverdate between '{start_date}-01-01' and '{end_date}-12-31'
            and title like '%{title}%'
            Order by PublisherName, title, issuenumber'''

    term = [title.lower()]
    results = ComicData(wishlist=False, query=query)
    results = results.parse_data(wishlist=False)

    comics = ComicData(wishlist=False, query=None)
    comics = comics.parse_data(wishlist=False)

    advanced_form = AdvancedForm2()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_collection', title=search_form.search_text.data))

        elif advanced_form.submit3.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_collection', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data, graded=advanced_form.graded.data))
    return render_template('collection.html', theme=theme, search_form=search_form,
                           advanced_form=advanced_form, comics=comics, start_date=start_date, end_date=end_date,
                           graded=graded, results=results, term=term,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


@app.route('/collection/<string:title>', methods=['GET', 'POST'])
def search_collection(title):
    titles = []
    theme = Colors.query.filter_by(selected=True).first()
    titles.append(title.lower())
    comics = ComicData(wishlist=False)
    comics = comics.parse_data(wishlist=False)

    advanced_form = AdvancedForm2()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.submit1.data and search_form.validate_on_submit:
            return redirect(url_for('search_collection', title=search_form.search_text.data))

        elif advanced_form.submit3.data and advanced_form.validate_on_submit:
            return redirect(url_for('advanced_search_collection', title=advanced_form.search_text.data,
                                    start_date=advanced_form.beginning_time.data,
                                    end_date=advanced_form.ending_time.data, graded=advanced_form.graded.data))
    return render_template('collection.html', theme=theme, search_form=search_form,
                           advanced_form=advanced_form, comics=comics, titles=titles,
                           year_options=generate_date_options(retrieve_oldest_comic_date(comics)))


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
        if wishlist == 'True':
            path = "wishlist(one_sheet).xlsx"
            return send_file(path, as_attachment=True)
        else:
            path = "collection(one_sheet).xlsx"
            return send_file(path, as_attachment=True)
    else:
        e.download_multi_sheet()
        if wishlist == 'True':
            path = "wishlist(multi_sheet).xlsx"
            return send_file(path, as_attachment=True)
        else:
            path = "collection(multi_sheet).xlsx"
            return send_file(path, as_attachment=True)


@app.context_processor
def inject_now():
    return {'now': int(dt.utcnow().strftime('%Y'))}

