"""
Access and Manage data from the MonogoDB Server

Guide ->
    Users: - User Information
        `getAllUsers()`
        `getLastUser()`
        `getUserByEmail(email)`
        `getUserByID(id)`
        `getUserByName(name)`
        `addUser(name, email, password)`
        `updateUser(name, email, password)`
    
    Stations:
        `getAllStations()`
        `getLastStation()`
        `addStation(
            name,
            registration,
            phone,
            email,
            coordinates,
            city,
            petrol,
            diesel,
            lastupdated,
            apetrol,
            adiesel,
            capacity_petrol,
            capacity_diesle
        )`
        `getByEmail(email)`
        `getByPhone(phone)`
        `getByRegistration(registration)`
        `getByID(id)`
        `getByCity(city)`
        `updateAvailability(id, petrol, diesel)`
        `updateAmount(id, petrol, diesel)`
    
    Pending:
        `getAllStations()`
        `getLastStation()`
        `addStation(
            name,
            registration,
            phone,
            email,
            coordinates,
            city,
            petrol,
            diesel,
            lastupdated,
            apetrol,
            adiesel,
            capacity_petrol,
            capacity_diesle, 
            lastupdated
        )`
        `getByEmail(email)`
        `getByPhone(phone)`
        `getByRegistration(registration)`
        `getByID(id)`
        `deleteByID(id)`
        `getByCity(city)`


Usage (Examples) ->
    from database.mongo import Users
    from database.mongo import Stations
    from database.mongo import Pending
    
    Users.getAllUsers()
    Stations.getAllStations()
    Pending.getAllStations()

"""


import typing as t
import urllib.parse
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from database.settings import MongoDB

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

    def getAllUsers() -> list:
        """
        return a list of all users
        """
        temp = []
        for user in users.find({}):
            temp.append(user)
        return temp

    def getLastUser():
        """
        return a dict with a user

        This is improvable and i dont know how to with pymongo
            https://stackoverflow.com/questions/32076382/mongodb-how-to-get-max-value-from-collections
        """
        temp = []
        for user in Users.getAllUsers():
            temp.append(user)
        return temp[-1]

    def getUserByEmail(email: t.Union[str, bytes]):
        """
        return a dict with a user
        """
        temp = []
        for user in users.find({'email': email}):
            temp.append(user)
        try:
            return temp[0]
        except:
            return False

    def getUserByID(id: t.Union[int, str]):
        """
        return a dict with a user
        """
        temp = []
        for user in users.find({'id': id}):
            temp.append(user)
        try:
            return temp[0]
        except:
            return False

    def getUserByName(name: t.Union[str, bytes]):
        """
        return a list of users
        """
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
        """
        add a new user if doesnt exist
        """
        try:
            temp = Users.getUserByEmail(email=email)
            if email == temp['email']:
                return
            else:
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
        except:
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
        "amount": {
            "petrol": "35",
            "diesel": "70"
        },
        "capacity": {
            "petrol": 123,
            "diesel": 123
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

    def addStation(
            name: t.Union[str, bytes],
            registration: t.Union[str, bytes],
            phone: t.Union[str, bytes],
            email: t.Union[str, bytes],
            coordinates: t.List[str],
            city: t.Union[str, bytes],
            petrol: bool,
            diesel: bool,
            lastupdated: t.Union[str, bytes],
            apetrol: str,
            adiesel: str,
            capacity_petrol,
            capacity_diesle,

    ):
        try:
            temp = Stations.getByRegistration(registration=registration)
            if temp['registration'] == registration:
                return
            else:
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
                            "amount": {
                                "petrol": apetrol,
                                "diesel": adiesel
                            },
                            "capacity": {
                                "petrol": capacity_petrol,
                                "diesel": capacity_diesle
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
                            "amount": {
                                "petrol": apetrol,
                                "diesel": adiesel
                            },
                            "capacity": {
                                "petrol": capacity_petrol,
                                "diesel": capacity_diesle
                            },
                            "lastupdated": lastupdated
                        }
                    )
        except:
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
                        "amount": {
                            "petrol": apetrol,
                            "diesel": adiesel
                        },
                        "capacity": {
                            "petrol": capacity_petrol,
                            "diesel": capacity_diesle
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
                        "amount": {
                            "petrol": apetrol,
                            "diesel": adiesel
                        },
                        "capacity": {
                            "petrol": capacity_petrol,
                            "diesel": capacity_diesle
                        },
                        "lastupdated": lastupdated
                    }
                )

    def getByEmail(email: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'email': email}):
            temp.append(station)
        return temp

    def getByPhone(phone: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'phone': phone}):
            temp.append(station)
        return temp

    def getByRegistration(registration: t.Union[str, bytes]):
        temp = []
        for station in stations.find({'registration': registration}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False

    def getByID(id: t.Any):
        temp = []
        for station in stations.find({'id': int(id)}):
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

    def updateAvailability(id: int, petrol: bool, diesel: bool):
        stations.find_one_and_update(
            {
                "id": id
            },
            {
                "$set": {
                    'availablitiy': {
                        'petrol': petrol,
                        'diesel': diesel
                    },
                    'lastupdated': datetime.now()
                }
            },
            upsert=True
        )
        return True

    def updateAmount(id: int, petrol: str, diesel: str):
        stations.find_one_and_update(
            {
                "id": id
            },
            {
                "$set": {
                    'amount': {
                        'petrol': petrol,
                        'diesel': diesel
                    },
                    'lastupdated': datetime.now()
                }
            },
            upsert=True
        )
        return True


class Pending:
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
        "capacity": {
            "petrol": 123,
            "diesel": 123
        },
        "image": "",
        "lastupdated": ""
    }
    """

    def getAllStations():
        temp = []
        for station in pending.find({}):
            temp.append(station)
        return temp

    def getLastStation():
        """
        This is improvable and i dont know how to with pymongo
            https://stackoverflow.com/questions/32076382/mongodb-how-to-get-max-value-from-collections
        """
        temp = []
        for user in Pending.getAllStations():
            temp.append(user)
        return temp[-1]

    def addStation(
        name: t.Union[str, bytes],
        registration: t.Union[str, bytes],
        phone: t.Union[str, bytes],
        email: t.Union[str, bytes],
        coordinates: t.List[str],
        city: t.Union[str, bytes],
        petrol: bool,
        diesel: bool,
        image: t.Union[str, bytes],
        capacity_petrol,
        capacity_diesle,
        lastupdated
    ):
        try:
            temp = Pending.getByRegistration(registration=registration)
            if temp['registration'] == registration:
                return
            else:
                try:
                    pending.insert_one(
                        {
                            'id': int(Pending.getLastStation()['id']) + 1,
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
                            "capacity": {
                                "petrol": capacity_petrol,
                                "diesel": capacity_diesle
                            },
                            "image": image,
                            "lastupdated": str(datetime.now())
                        }
                    )
                except IndexError:
                    pending.insert_one(
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
                            "capacity": {
                                "petrol": capacity_petrol,
                                "diesel": capacity_diesle
                            },
                            "image": image,
                            "lastupdated": str(datetime.now())
                        }
                    )
        except:
            try:
                pending.insert_one(
                    {
                        'id': int(Pending.getLastStation()['id']) + 1,
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
                        "capacity": {
                            "petrol": capacity_petrol,
                            "diesel": capacity_diesle
                        },
                        "image": image,
                        "lastupdated": str(datetime.now())
                    }
                )
            except IndexError:
                pending.insert_one(
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
                        "capacity": {
                            "petrol": capacity_petrol,
                            "diesel": capacity_diesle
                        },
                        "image": image,
                        "lastupdated": str(datetime.now())
                    }
                )

    def getByEmail(email: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'email': email}):
            temp.append(station)
        return temp

    def getByPhone(phone: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'phone': phone}):
            temp.append(station)
        return temp

    def getByRegistration(registration: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'registration': registration}):
            temp.append(station)
        return temp[0]

    def getByID(id: t.Union[int, str, bytes]):
        temp = []
        for station in pending.find({'id': int(id)}):
            temp.append(station)
        return temp[0]

    def deleteByID(id: t.Union[int, str, bytes]):
        pending.delete_one({"id": int(id)})

    def getByCity(city: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'city': city}):
            temp.append(station)
        return temp
