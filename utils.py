from comic_wishlist import db
from comic_wishlist.models import Colors, Comics, Issues, Presses

colors = {
    'steel': ['#14213d', '#fca311', '#282e3c', '#fca311', '#284b63'],
    'blue': ['#7EA3CC', '#B3001B', '#262626', '#255C99', '#CEDFF3'],
}


def add_color():
    for k, v in colors.items():
        color = Colors(name=k, selected=False, bgcolor=v[0], primary=v[1],
                      secondary=v[2], third=v[3], mute=v[4])

        db.session.add(color)


presses = ['Marvel', 'DC', 'A03']

def add_press():
    for x in presses:
        press = Presses(name=x)
        db.session.add(press)
        db.session.commit()


comics = {
    'ironman': [1],
    'x-men': [1],
    'superman': [2]
}

def add_comic():
    for k, v in comics.items():
        comic = Comics(title=k, press=v[0])

        db.session.add(comic)


issues = {
    'ironman vs cap #109': ['109', 2009, 1],
    'ironman vs cap #809': ['809', 2020, 1],
    'x-men special': ['400', 1996, 2],
    'superman loves batman': ['10000', 2005, 3]
}


def add_issue():
    for k, v in issues.items():
        issue = Issues(sub_title=k, number=v[0], year=v[1], comic_id=v[2])
        db.session.add(issue)





db.session.commit()
add_color()
add_comic()
add_issue()
add_press()

