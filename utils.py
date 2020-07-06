from comic_wishlist import db
from comic_wishlist.models import Color

colors = {
    'ironman': ['f0f0f4', 'AA0505', '6A0C0B', 'B97D10', 'FBCA03'],
    'capmarvel': ['f0f0f4', '2A75B3', 'F3D403', '000000', 'CC4224'],


}


def add_color():
    for k, v in colors.items():
        theme = Color(name=k, bgcolor=v[0], primary=v[1],
                      secondary=v[2], third=v[3], mute=v[4])

        print(theme)
        db.session.add(theme)
        db.session.commit()

add_color()

