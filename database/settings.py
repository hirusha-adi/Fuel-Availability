import os
import json
import re
import typing as t



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
FILENAME_ENV = os.path.join(os.getcwd(), '.env')
FILENAME_ENV_new = os.path.join(os.getcwd(), '.env.old')

def get_env(name: str, default: t.Optional[t.Union[str,int,bool]] = None) -> t.Union[int,str,bool]:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
            os.system('pip install python-dotenv' if os.name == 'nt' else 'pip3 install python-dotenv')
            from dotenv import load_dotenv
            load_dotenv()
    value: str | None = os.getenv(name, None)
    if value is None:
        if default is None:
            return "ERROR"
        else:
            return default
    else:
        if (name == 'WEBSERVER_HOST') or (name == 'MYSQL_IP'):
            ipv4_regex = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            if re.match(ipv4_regex, value):
                return str(value)
            
        elif name == 'WEBSERVER_PORT':
            port_regex = r"^[1-9]\d{0,3}$|^0$|^6553[0-5]$|^655[0-2]\d$|^65[0-4]\d{2}$|^6[0-4]\d{3}$|^[1-5]\d{4}$|^6[0-5][0-4][0-9]{2}$"
            if re.match(port_regex, value):
                return str(value)
            
        elif name == 'WEBSERVER_DEBUG':
            true_ = ('true', '1', 't', 'on', 'e', 'enable')
            if value in true_:
                return True
            else:            
                return False 
            
        elif (name == 'CONTACT_EMAIL') or (name == 'ADMIN_EMAIL') or (name == 'ADMIN_USERNAME'):
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if re.match(email_regex, value):
                return str(value)
        
        elif name == 'ADMIN_ID':
            try:
                return int(value) 
            except:
                if default is None:
                    return 7879
                else:
                    return default
        else:
            return str(value)

def init():
    if os.path.isfile(FILENAME_ENV):
        print("[+] Found '.env' file, loading and dumping data to './database/settings.json'")
        FLASK_SECRET: str = get_env('FLASK_SECRET', None)
        JAWG_TOKEN: str = get_env('JAWG_TOKEN', None)
        CONTACT_EMAIL: str = get_env('CONTACT_EMAIL', 'hirushaadi@gmail.com')
        
        WEBSERVER_HOST: str = get_env('WEBSERVER_HOST', '0.0.0.0')
        WEBSERVER_PORT: str = get_env('WEBSERVER_PORT', "7879")
        WEBSERVER_DEBUG: bool = get_env('WEBSERVER_DEBUG', False)
        
        ADMIN_ID: int  = get_env('ADMIN_ID', None)
        ADMIN_FULLNAME: str  = get_env('ADMIN_FULLNAME', None)
        ADMIN_USERNAME: str  = get_env('ADMIN_USERNAME', None)
        ADMIN_EMAIL: str  = get_env('ADMIN_EMAIL', None)
        ADMIN_PASSWORD: str  = get_env('ADMIN_PASSWORD', None)
        
        MYSQL_IP: str  = get_env('MYSQL_IP', "localhost")
        MYSQL_USERNAME: str  = get_env('MYSQL_USERNAME', None)
        MYSQL_PASSWORD: str  = get_env('MYSQL_PASSWORD', None)
        MYSQL_PORT: int  = get_env('MYSQL_PORT', 3306)
        MYSQL_DATABASE: str  = get_env('MYSQL_DATABASE', "fuelapp")
        
        with open(FILENAME, 'w', encoding='utf-8') as file:
            tmp = {
                "webserver": {
                    "host": WEBSERVER_HOST,
                    "port": WEBSERVER_PORT,
                    "debug": WEBSERVER_DEBUG
                },
                "admin": {
                    "id": ADMIN_ID,
                    "fullname": ADMIN_FULLNAME,
                    "username": ADMIN_USERNAME,
                    "email": ADMIN_EMAIL,
                    "password": ADMIN_PASSWORD
                },
                "flaskSecret": FLASK_SECRET,
                "JawgToken": JAWG_TOKEN,
                "contactEmail": CONTACT_EMAIL,
                "mysql": {
                    "ip": MYSQL_IP,
                    "port": MYSQL_PORT,
                    "username": MYSQL_USERNAME,
                    "password": MYSQL_PASSWORD,
                    "database": MYSQL_DATABASE
                }
            }
            json.dump(tmp, file, indent=4)
        
        os.rename(FILENAME_ENV, FILENAME_ENV_new)
    
    else:
        print("[+] '.env' file not found, defaulting to settings.json")
        

init() # run this initially

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


class MySQL:
    mysql = data["mysql"]
    
    ip: str = mysql["ip"]
    
    def uip(new: str):
        MySQL.ip = new
        data['mysql']['ip'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
    
    port: int = mysql["port"]
    
    def uport(new: str):
        MySQL.port = new
        data['mysql']['port'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
        
    username: str = mysql["username"]
    
    def uusername(new: str):
        MySQL.username = new
        data['mysql']['username'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
            
    password: str = mysql["password"]
    
    def upassword(new: str):
        MySQL.password = new
        data['mysql']['password'] = new
        with open(FILENAME, "w") as sf:
            json.dump(data, sf, indent=4)
    
    database: str = mysql["database"]
    
    def udatabase(new: str):
        MySQL.database = new
        data['mysql']['database'] = new
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


        
