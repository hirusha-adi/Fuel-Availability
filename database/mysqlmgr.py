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
        `updateUserNewEmail(name, email, newEmail, password)`
        `deleteByID(id)`
    
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
        `updateStation(
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

from database.settings import MySQL

# users = client['fuel']['users']
# stations = client['fuel']['stations']
# pending = client['fuel']['pending']

import mysql.connector

def makeConnection():
    try:
        connection = mysql.connector.connect(
            # host=MySQL.ip,
            host="localhost",
            user=MySQL.username,
            password=MySQL.password,
            port=MySQL.port,
            database=MySQL.database
        )
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None

client = makeConnection()

def initDataBase(connection):
    if connection is not None:
        ddl_list = [
    """
    CREATE TABLE `Server`(
        `flask_secret` VARCHAR(255) NOT NULL,
        `jawg_token` VARCHAR(255) NOT NULL,
        `contact_email` VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE `Users`(
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL,
        `email` VARCHAR(255) NOT NULL,
        `password` VARCHAR(255) NOT NULL
    )
    """,
    """
    ALTER TABLE `Users` ADD UNIQUE `users_email_unique`(`email`)
    """,
    """
    CREATE TABLE `Stations` (
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `user_id` BIGINT NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        `phone` VARCHAR(255) NOT NULL,
        `registration` BIGINT NOT NULL,
        `google_maps_url` LONGTEXT NOT NULL,
        `co_lon` BIGINT NOT NULL,
        `co_lat` BIGINT NOT NULL,
        `available_petrol` BOOLEAN NOT NULL,
        `available_diesel` BOOLEAN NOT NULL,
        `capacity_petrol` SMALLINT NULL,
        `capacity_diesel` SMALLINT NULL,
        `last_updates` DATETIME NULL,
        `is_pending` BOOLEAN
    );
    """,
    """
    CREATE TABLE `Admins`(
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `full_name` VARCHAR(255) NULL,
        `username` VARCHAR(255) NULL,
        `email` VARCHAR(255) NOT NULL,
        `password` VARCHAR(255) NOT NULL
    )
    """,
    """
    ALTER TABLE `Stations` ADD CONSTRAINT `stations_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
    """
]
        try:
            cursor = connection.cursor()
            for ddl in ddl_list:
                try:
                    cursor.execute(ddl)
                    print("[+] DDL Executed:", ddl)
                except Exception as e:
                    print("[!!] Error executing DDL:", ddl)
        except mysql.connector.Error as error:
            print("Error executing DDL statements:", error)

class Users:
    """
+----------+-----------------+------+-----+---------+----------------+
| Field    | Type            | Null | Key | Default | Extra          |
+----------+-----------------+------+-----+---------+----------------+
| id       | bigint unsigned | NO   | PRI | NULL    | auto_increment |
| name     | varchar(255)    | NO   |     | NULL    |                |
| email    | varchar(255)    | NO   | UNI | NULL    |                |
| password | varchar(255)    | NO   |     | NULL    |                |
+----------+-----------------+------+-----+---------+----------------+
    """

    def getAllUsers(connection):
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users")
                users = cursor.fetchall()
                cursor.close()
                return users
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None

    def getLastUser(connection):
        """
        return a dict with a user that was added lastly
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users ORDER BY id DESC LIMIT 1")
                user = cursor.fetchone()
                cursor.close()
                return user
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None

    def getUserByEmail(connection, email: t.Union[str, bytes], all=False):
        """
        return a dict with a user
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
                user = cursor.fetchone()
                cursor.close()
                return user
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None
    
    def getUserByPassword(connection, password: t.Union[str, bytes], all=False):
        """
        return a dict with a user
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users WHERE password = %s", (password,))
                user = cursor.fetchone()
                cursor.close()
                return user
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None

    def getUserByID(connection, id: t.Union[int, str], all=False):
        """
        return a dict with a user
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users WHERE id = %s", (id,))
                user = cursor.fetchone()
                cursor.close()
                return user
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None

    def getUserByName(connection, name: t.Union[str, bytes], all=False):
        """
        return a list of users
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users WHERE name = %s", (name,))
                user = cursor.fetchone()
                cursor.close()
                return user
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
                return None

    def addUser(connection, name: t.Union[str, bytes], email: t.Union[str, bytes], password: t.Union[str, bytes]):
        """
        add a new user if doesnt exist
        """
        if connection is not None:
            try:
                cursor = connection.cursor()
                add_user_query = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(add_user_query, (name, email, password))
                cursor.close()
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
        

    def updateUser(connection, name: t.Union[str, bytes], email: t.Union[str, bytes], password: t.Union[str, bytes]):
        if connection is not None:
            try:
                cursor = connection.cursor()
                update_user_query = "UPDATE Users SET name = %s, password = %s WHERE email = %s"
                cursor.execute(update_user_query, (name, password, email))
                cursor.close()
                return True
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)
    
    def updateUserNewEmail(connection, name: t.Union[str, bytes], email: t.Union[str, bytes], newEmail: t.Union[str, bytes], password: t.Union[str, bytes]):
        if connection is not None:
            try:
                cursor = connection.cursor()
                update_user_email_query = "UPDATE Users SET email = %s WHERE name = %s AND email = %s AND password = %s"
                cursor.execute(update_user_email_query, (newEmail, name, email, password))
                cursor.close()
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)

    def deleteByID(connection, id: t.Union[int, str, bytes]):
        if connection is not None:
            try:
                cursor = connection.cursor()
                delete_user_query = "DELETE FROM Users WHERE id = %s"
                cursor.execute(delete_user_query, (id,))
                cursor.close()
            except mysql.connector.Error as error:
                print("Error fetching all users:", error)

class Stations:
    """
+------------------+-----------------+------+-----+---------+----------------+
| Field            | Type            | Null | Key | Default | Extra          |
+------------------+-----------------+------+-----+---------+----------------+
| id               | bigint unsigned | NO   | PRI | NULL    | auto_increment |
| user_id          | bigint          | NO   |     | NULL    |                |
| name             | varchar(255)    | NO   |     | NULL    |                |
| phone            | varchar(255)    | NO   |     | NULL    |                |
| registration     | bigint          | NO   |     | NULL    |                |
| google_maps_url  | longtext        | NO   |     | NULL    |                |
| co_lon           | bigint          | NO   |     | NULL    |                |
| co_lat           | bigint          | NO   |     | NULL    |                |
| available_petrol | tinyint(1)      | YES  |     | NULL    |                |
| available_diesel | tinyint(1)      | YES  |     | NULL    |                |
| capacity_petrol  | smallint        | YES  |     | NULL    |                |
| capacity_diesel  | smallint        | YES  |     | NULL    |                |
| last_updates     | datetime        | YES  |     | NULL    |                |
| is_pending       | tinyint(1)      | YES  |     | NULL    |                |
+------------------+-----------------+------+-----+---------+----------------+
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

    def updateStation(
            id: int, 
            
            # Updated using web UI
            name: t.Union[str, bytes],
            registration: t.Union[str, bytes],
            phone: t.Union[str, bytes],
            email: t.Union[str, bytes],
            coordinates: t.Union[str, t.List[str]],
            city: t.Union[str, bytes],
            
            # Not updated using web UI
            apetrol: str=None,
            adiesel: str=None,
            diesel: bool=None,
            petrol: bool=None,
            capacity_petrol=None,
            capacity_diesle=None
        ):
        
        if (apetrol is None) or (adiesel is None) or (diesel is None) or (petrol is None) or (capacity_petrol is None) or (capacity_diesle is None):
            missing_data = Stations.getByID(id=id)
        
        if isinstance(coordinates, str):
            coordinates = coordinates.split(",")
        
        stations.find_one_and_update(
            {
                "id": id
            },
            {
                "$set": {
                        'id': 1,
                        "name": name,
                        "registration": registration,
                        "phone": phone,
                        "email": email,
                        "coordinates": coordinates,
                        "city": city,
                        "availablitiy": {
                            "petrol": petrol or missing_data['availablitiy']['petrol'],
                            "diesel": diesel or missing_data['availablitiy']['diesel']
                        },
                        "amount": {
                            "petrol": apetrol or missing_data['amount']['petrol'],
                            "diesel": adiesel or missing_data['amount']['diesel']
                        },
                        "capacity": {
                            "petrol": capacity_petrol or missing_data['capacity']['petrol'],
                            "diesel": capacity_diesle or missing_data['capacity']['diesel']
                        },
                        'lastupdated': datetime.now()
                }
            },
            upsert=True
        )
        return True
    
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

    def getByName(name: t.Any):
        temp = []
        for station in stations.find({'name': str(name)}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False
    
    def getByCoordinates(coordinates: t.Any):
        temp = []
        coordinates_list = str(coordinates).split(",") 
        for station in stations.find({'coordinates': coordinates_list}):
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

    def deleteByID(id: t.Union[int, str, bytes]):
        stations.delete_one({"id": int(id)})

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

    def getByCoordinates(coordinates: t.Any):
        temp = []
        coordinates_list = str(coordinates).split(",") 
        for station in pending.find({'coordinates': coordinates_list}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False

    def getByName(name: t.Any):
        temp = []
        for station in pending.find({'name': str(name)}):
            temp.append(station)
        try:
            return temp[0]
        except:
            return False
    
    def getByEmail(email: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'email': email}):
            temp.append(station)
        return temp

    def getByImage(image: t.Union[str, bytes]):
        temp = []
        for station in pending.find({'image': image}):
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
