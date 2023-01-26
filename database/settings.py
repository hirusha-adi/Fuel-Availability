import os
import json

FILENAME = os.path.join(os.getcwd(), 'database', 'settings.json')

with open(FILENAME, 'r', encoding='utf-8') as _file:
    data = json.load(_file)

flaskSecret = data['flaskSecret']

def uflaskSecret(new):
    global flaskSecret
    flaskSecret = new
    data['flaskSecret'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)

JawgToken = data['JawgToken']

def uJawgToken(new):
    global JawgToken
    JawgToken = new
    data['JawgToken'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)
        
contactEmail = data['contactEmail']

def ucontactEmail(new):
    global contactEmail
    contactEmail = new
    data['contactEmail'] = new
    with open(FILENAME, "w") as sf:
        json.dump(data, sf, indent=4)

uploadPath = os.path.join(os.getcwd(), 'static', 'uploads')
if not (os.path.isdir(uploadPath)):
    os.makedirs(uploadPath)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


class MongoDB:
    mongodb = data["mongodb"]
    
    ip: str = mongodb["ip"]
    
    def uip(new):
        MongoDB.ip = new
        data['mongodb']['ip'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
        
    username: str = mongodb["username"]
    
    def uusername(new):
        MongoDB.username = new
        data['mongodb']['username'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
    password: str = mongodb["password"]
    
    def upassword(new):
        MongoDB.password = new
        data['mongodb']['password'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
    

class WebServer:
    webserver = data["webserver"]
    
    host = webserver['host']
    
    def uhost(new):
        WebServer.host = new
        data['webserver']['host'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
    port = webserver['port']
    
    def uport(new):
        WebServer.port = new
        data['webserver']['port'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
            
    debug = webserver['debug']
    
    def udebug(new):
        WebServer.debug = new
        data['webserver']['debug'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)

class Admin:
    admin = data["admin"]
    username = admin['username']
    email = admin['email']
    id = admin['id']
    password = admin['password']
    fullname = admin['fullname']
    