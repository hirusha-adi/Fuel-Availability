
import urllib.parse
from pymongo import MongoClient
from bson import ObjectId
from database.settings import MongoDB

client = MongoClient('mongodb://%s:%s@%s:27017/' % (
    urllib.parse.quote_plus(MongoDB.username),
    urllib.parse.quote_plus(MongoDB.password),
    MongoDB.ip
))

users = client['users']['users']


class Users:
    """
    {
        "_id": {
            "$oid": ""
        },
        "id": 1,
        "name": "",
        "email": "",
        "password": ""
    }
    """

    def getAllUsers():
        temp = []
        for user in users.find({}):
            temp.append(user)
        return temp

    def getLastUser():
        """
        This is improvable and i dont know how to with pymongo
            https://stackoverflow.com/questions/32076382/mongodb-how-to-get-max-value-from-collections
        """
        temp = []
        for user in Users.getAllUsers():
            temp.append(user)
        return temp[-1]

    def getUserByEmail(email: str):
        temp = []
        for user in users.find({'email': email}):
            temp.append(user)
        try:
            return temp[0]
        except:
            return False

    def getUserByID(id):
        temp = []
        for user in users.find({'id': id}):
            temp.append(user)
        return temp[0]

    def getUserByName(name: str):
        temp = []
        for user in users.find(
            {
                "name": {
                    "$regex": f'.*{name}*.',
                    "$options": 'i'  # ignore case
                }
            }
        ):
            temp.append(user)
        return temp

    def addUser(name, email, password):
        try:
            users.insert_one(
                {
                    'id': int(Users.getLastUser()['id']) + 1,
                    'name': name,
                    'email': email,
                    'password': password
                }
            )
        except IndexError:
            users.insert_one(
                {
                    'id': 1,
                    'name': name,
                    'email': email,
                    'password': password
                }
            )

    def updateUser(name, email, password):
        users.find_one_and_update(
            {
                "email": email
            },
            {
                "$set": {
                    'name': name,
                    'email': email,
                    'password': password
                }
            },
            upsert=True
        )
        return True
