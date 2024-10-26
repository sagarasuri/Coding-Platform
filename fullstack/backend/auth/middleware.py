import functools
from flask import session,redirect

def auth(view_func):
    @functools.wraps(view_func)
    def  decorated(*args,**kwargs):
        if 'email' not in session:
            return redirect('./login')
        return view_func(*args,**kwargs)
    return decorated


def guest(view_func):
    @functools.wraps(view_func)
    def  decorated(*args,**kwargs):
        if 'email' in session:
            return redirect('./dashboard')
        return view_func(*args,**kwargs)
    return decorated