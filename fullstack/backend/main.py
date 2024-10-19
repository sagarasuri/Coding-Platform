from pymongo import MongoClient
from bson.objectid import ObjectId


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)

    db = client['your_database_name']

    user_id = ObjectId('6706a1c7a0103a2283599c71')

    # Directly use ObjectId for querying
    post_id = db.users.find_one({'_id': user_id})

    print(post_id['name'])