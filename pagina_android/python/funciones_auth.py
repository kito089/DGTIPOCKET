from flask import session, render_template#, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("----------entre?")
        user = session.get('profile', {})
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            print("---------usuario encontrado")
            return f(*args, **kwargs)
        print("----------usuario no encontrado, rediriguendo a login")
        return render_template("/login")#'You aint logged in, no page for u!'
    return decorated_function