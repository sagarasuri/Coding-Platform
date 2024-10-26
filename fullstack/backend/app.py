from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask_cors import CORS
import sys
sys.path.append('fullstack/backend/auth')

from auth.middleware1 import create_access_token, check_password_hash, generate_password_Hash,auth_required
from flask_jwt_extended import create_access_token as jwt_create_access_token
from bson import ObjectId



app = Flask(__name__)
CORS(app, support_credentials=True)


client = MongoClient("localhost", 27017)
db = client['my_db']
collection = db.users


app.config['JWT_SECRET_KEY'] = 'Sagar@123'
jwt = JWTManager(app)

@app.route('/')
def home():
    return "Welcome to the user management API."

@app.route('/registration', methods=['POST'])
def store_user_data():
    userData = request.get_json()
    #print(userData)
    username = userData.get("userName")
    password = userData.get("password")
    email=userData.get("email")
    phoneNumber=userData.get("phoneNo")

    # print('hello world')
    if collection.find_one({"username": username}):
        return jsonify({"msg": "User already exists!"}), 400

    hashed_password = generate_password_Hash(password)
    user_data = {
        "username": username,
        "password": hashed_password,
        "email":email,
        "phoneNo":phoneNumber,
    }
    try:
        user_data=collection.insert_one(user_data)
        inserted_id=user_data.inserted_id
        inserted_id_str=str(inserted_id)
        access_token=create_access_token(inserted_id_str)
        return jsonify({"access_token":access_token}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def user_login(): 
    data = request.get_json()
    print(data)
    email = data.get("email")
    password = data.get("password")
    user = collection.find_one({"email": email})
    print(collection.find_one({"email": email}))
    print(user)
    if user: # and check_password_hash(user['password'], password):
        return jsonify({"msg":"User logged in Successfully"}), 200
    else:
        return jsonify({"msg": "Invalid credentials!"}), 401


@app.route('/dashboard', methods=['GET'])
@auth_required
def redirect_to_dashboard():
    current_user = get_jwt_identity()  
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True)
