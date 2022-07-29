import os
import json

with open(os.path.join(os.getcwd(), 'database', 'settings.json'), 'r', encoding='utf-8') as _file:
    data = json.load(_file)


class MongoDB:
    mongodb = data["mongodb"]
    ip: str = mongodb["ip"]
    username: str = mongodb["username"]
    password: str = mongodb["password"]
