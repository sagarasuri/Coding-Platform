from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_jwt_extended import create_access_token as jwt_create_access_token

def create_access_token(identity):
    # Call the actual JWT library function to create a token
    return jwt_create_access_token(identity=identity)


def check_user_credentials(username, password, user_collection):
    user = user_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return True
    return False

def generate_password_Hash(password):
    return generate_password_hash(password)


def auth_required(f):
    @wraps(f)
    def decorated_function():
        if 'logged_in' not in session or not session['logged_in']:
            return redirect('/login')
        return f(*args,**kwargs)
    return decorated_function
    