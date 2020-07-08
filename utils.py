from comic_wishlist import db
from comic_wishlist.models import Colors

colors = {
    'steel': ['#14213d', '#fca311', '#282e3c', '#fca311', '#284b63'],
    'blue': ['#7EA3CC', '#B3001B', '#262626', '#255C99', '#CEDFF3'],
}


def add_color():
    for k, v in colors.items():
        color = Colors(name=k, selected=False, bgcolor=v[0], primary=v[1],
                      secondary=v[2], third=v[3], mute=v[4])

        db.session.add(color)
        db.session.commit()


add_color()



