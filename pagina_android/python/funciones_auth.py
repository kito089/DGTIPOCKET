from flask import session, render_template, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("------entre")
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            print("---------usuario encontrado")
            if str.isnumeric(user['email'][0]):
                user.update({'persona':'alumno'})
            else:
                user.update({'persona':'maestro'})
            return f(*args, **kwargs)
        print("----------usuario no encontrado, rediriguendo a login")
        return redirect(url_for("login"))
    return decorated_function