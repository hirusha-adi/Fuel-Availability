import os
import json

"""
Has all the variables and has functions to update them properly

Guide ->
    Main Settings
        - Access:
            `flaskSecret`: Flask Secret Key
            `JawgToken`:  Jawg Token - You can get it from https://www.jawg.io/lab/access-tokens
            `contactEmail`: Contact Us Email Address
        - Update
            `uflaskSecret(new)`: Update Flask Secret Key
            `uJawgToken(new)`: Update the Jawg Token
            `ucontactEmail(new)`: Update the Contact Us Email Address

    Mongo Settings
        - Access
            `ip`: Server IP
            `username`: Login Username
            `password`: Login Password
        - Update
            `uip`: Update Server IP
            `uusername`: Update Login Username 
            `upassword`: Update Login Password 

    Web Server Settings
        - Access
            `host`: IP Address to Start Flask Server
            `port`: Port to Start Flask Server
            `debug`: Use Debug Mode with Flask Server?
        - Update
            `uhost`: Update IP Address to Start Flask Server
            `uport`: Update Port to Start Flask Server
            `udebug`: Upsate weather to use Debug Mode with Flask Server?

    Admin Settings
        - Access
            `id`: User ID as in MongoDB Server 
            `username`: Username as in MongoDB Server (should be same as email) 
            `email`: Email as in MongoDB Server 
            `password`: Password as in MongoDB Server 
            `fullname`: Full Name as in MongoDB Server 
        - Update
            CANNOT UPDATE THEM VIA THE WEB UI
                
Usage (Examples) ->
    1.  from database import settings
    
        print(settings.JawgToken)
        print(settings.MongoDB.ip)
        
        settings.uJawgToken(new="TOKEN")
        settings.MongoDB.uip(new="0.0.0.0")
    
    
    2.  from database.settings import JawgToken
        from database.settings import uJawgToken
        from database.settings import MongoDB
        from database.settings.MongoDB import uip
        
        print(JawgToken)
        print(MongoDB.ip)
        
        uJawgToken(new="TOKEN")
        uip(new="0.0.0.0")
"""

FILENAME = os.path.join(os.getcwd(), 'database', 'settings.json')

with open(FILENAME, 'r', encoding='utf-8') as _file:
    data = json.load(_file)

flaskSecret: str = data['flaskSecret']

def uflaskSecret(new: str):
    global flaskSecret
    flaskSecret = new
    data['flaskSecret'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)

JawgToken: str = data['JawgToken']

def uJawgToken(new: str):
    global JawgToken
    JawgToken = new
    data['JawgToken'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)
        
contactEmail: str = data['contactEmail']

def ucontactEmail(new: str):
    global contactEmail
    contactEmail = new
    data['contactEmail'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)

uploadPath = os.path.join(os.getcwd(), 'static', 'uploads')
if not (os.path.isdir(uploadPath)):
    os.makedirs(uploadPath)

ALLOWED_EXTENSIONS: set = set(['pdf', 'png', 'jpg', 'jpeg'])


class MongoDB:
    mongodb = data["mongodb"]
    
    ip: str = mongodb["ip"]
    
    def uip(new: str):
        MongoDB.ip = new
        data['mongodb']['ip'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
        
    username: str = mongodb["username"]
    
    def uusername(new: str):
        MongoDB.username = new
        data['mongodb']['username'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
    password: str = mongodb["password"]
    
    def upassword(new: str):
        MongoDB.password = new
        data['mongodb']['password'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
    

class WebServer:
    webserver = data["webserver"]
    
    host: str = webserver['host']
    
    def uhost(new: str):
        WebServer.host = new
        data['webserver']['host'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
    port: str = webserver['port']
    
    def uport(new: str):
        WebServer.port = new
        data['webserver']['port'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
            
    debug: str = webserver['debug']
    
    def udebug(new: str):
        WebServer.debug = new
        data['webserver']['debug'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)

class Admin:
    admin = data["admin"]
    id: int = admin['id']
    username: str = admin['username']
    email: str = admin['email']
    password: str = admin['password']
    fullname: str = admin['fullname']
    