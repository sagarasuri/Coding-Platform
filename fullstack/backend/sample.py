from flask import Flask, render_template,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from bson import json_util
import sys
sys.path.append('utils')
from helpers import check_user_exists


# MongoDB connection (replace with your database details)
client = MongoClient("localhost", 27017)
db = client['my_db']
collection = db.users 

app = Flask(__name__)
CORS(app, support_credentials=True)
app.debug = True 

@app.route('/')
def insert_data():
    return "Data already inserted. Check /display to see entries."

@app.route('/display',methods=['POST'])
def display_data():
    documents = list(collection.find({}))
    queryData=request.args.get('name')
    return (queryData)

@app.route('/registration',methods=['POST'])
@cross_origin(supports_credentials=True)
def store_user_data():
    user_exists=False
    if not user_exists:
        try:
            userData=request.get_json()
            post_id=db.users.insert_one(userData)
            print(post_id)
        except:
            print('User already exists')

    else:
        return 'User already exists'
    return 'hi'


@app.route('/login',methods=['POST'])
@cross_origin(supports_credentials=True)
def user_login():
    userData=request.get_json()
    users_data=fetch_users().json
    is_user_exists=check_user_exists(users_data,userData)
    if is_user_exists:
        return True
    return False

@app.route('/fetchusersdata',methods=['GET'])
@cross_origin(supports_credentials=True)
def fetch_users():
    users_data = db.users.find()
    print(users_data)
    users_list = []
    for user in users_data:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users_list.append(user)
    return jsonify(users_list)

@app.route("/bad")
def bad():
    post_id = db.users.insert_one({'name': 'new user', 'age': 20, 'gender': 'male'})
    return f'The id of new user is: {post_id.inserted_id}'

@app.route("/debugged")
def debugged():
    resp = "This response is a string!"
    assert isinstance(resp, str), 'response must be a string'
    return resp

if __name__ == '__main__':
    app.run()
