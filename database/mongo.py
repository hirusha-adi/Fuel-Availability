
import urllib.parse
from pymongo import MongoClient
from bson import ObjectId
from database.settings import MongoDB
import typing as t

client = MongoClient('mongodb://%s:%s@%s:27017/' % (
    urllib.parse.quote_plus(MongoDB.username),
    urllib.parse.quote_plus(MongoDB.password),
    MongoDB.ip
))

users = client['fuel']['users']
stations = client['fuel']['stations']
pending = client['fuel']['pending']


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

    def getUserByEmail(email: t.Union[str, bytes]):
        temp = []
        for user in users.find({'email': email}):
            temp.append(user)
        try:
            return temp[0]
        except:
            return False

    def getUserByID(id: t.Union[int, str]):
        temp = []
        for user in users.find({'id': id}):
            temp.append(user)
        return temp[0]

    def getUserByName(name: t.Union[str, bytes]):
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

    def addUser(name: t.Union[str, bytes], email: t.Union[str, bytes], password: t.Union[str, bytes]):
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

    def updateUser(name: t.Union[str, bytes], email: t.Union[str, bytes], password: t.Union[str, bytes]):
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


class Stations:
    """
    {
        "_id": {
            "$oid": ""
        },
        "id": 1,
        "name": "Dhammika Filling Station",
        "phone": "0719999999",
        "email": "hirusha@hirusha.xyz",
        "registration": "123",
        "coordinates": [
            7.494112,
            80.3679604
        ],
        "city": "Kurunegala",
        "availablitiy": {
            "petrol": true,
            "diesel": false
        },
        "lastupdated": ""
    }
    """

    def getAllStations():
        temp = []
        for station in stations.find({}):
            temp.append(station)
        return temp

    def getLastStation():
        """
        This is improvable and i dont know how to with pymongo
            https://stackoverflow.com/questions/32076382/mongodb-how-to-get-max-value-from-collections
        """
        temp = []
        for user in Stations.getAllStations():
            temp.append(user)
        return temp[-1]

    def addStation(name: t.Union[str, bytes], registration: t.Union[str, bytes], phone: t.Union[str, bytes], email: t.Union[str, bytes], coordinates: t.List[str], city: t.Union[str, bytes], petrol: bool, diesel: bool, lastupdated: t.Union[str, bytes]):
        try:
            stations.insert_one(
                {
                    'id': int(Stations.getLastStation()['id']) + 1,
                    "name": name,
                    "registration": registration,
                    "phone": phone,
                    "email": email,
                    "coordinates": coordinates,
                    "city": city,
                    "availablitiy": {
                        "petrol": petrol,
                        "diesel": diesel
                    },
                    "lastupdated": lastupdated
                }
            )
        except IndexError:
            stations.insert_one(
                {
                    'id': 1,
                    "name": name,
                    "registration": registration,
                    "phone": phone,
                    "email": email,
                    "coordinates": coordinates,
                    "city": city,
                    "availablitiy": {
                        "petrol": petrol,
                        "diesel": diesel
                    },
                    "lastupdated": lastupdated
                }
            )

    def getByEmail(email: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'email': email}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False

    def getByPhone(phone: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'phone': phone}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False

    def getByRegistration(registration: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'registration': registration}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False

    def getByCity(city: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'city': city}):
            temp.append(station)
        return temp
