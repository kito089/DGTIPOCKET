from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        if user:
            print("---------usuario encontrado")
            #print(user)
            return f(*args, **kwargs)
        #print("----------usuario no encontrado, rediriguendo a login")
        return redirect(url_for("carga"))
    return decorated_function

def creds_required(f):
    @wraps(f)
    def decorated_functions(*args, **kwargs):
        creden = dict(session).get('profile', None)
        if creden:
            print("---------credenciales encontradas")
            #print(creden)
            return f(*args, **kwargs)
        print("----------credenciales no encontradas, rediriguendo a login")
        return redirect(url_for("carga"))
    return decorated_functions