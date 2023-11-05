import os
import json
import uvicorn
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class DB:
    def __init__(self):
        self.data = {}
        
    def create_DB(self, DB_name, DB_type):
        self.data[DB_name] = DB_type(DB_name)
        return
    def remove_DB(self, DB_name):
        del self.data[DB_name]
        return
    def add_data(self, DB_name, data):
        self.data[DB_name].add_data(data)
        return
    def get_data(self, DB_name):
        return self.data[DB_name].get_data()
    def remove_data(self, DB_name, data=None):
        self.data[DB_name].remove_data(data)
        return
    

class sorted_list_DB_type:
    def __init__(self, DB_name):
        self.data = []
        self.db_info = {
            'DB_name': DB_name,
            'DB_length': 0
        }
    def add_data(self, data):
        self.data.append(data)
        self.db_info['DB_length'] += 1
        return
    def remove_data(self, index):
        if index == None:
            index = -1
        del self.data[index]
        self.db_info['DB_length'] -= 1
        return
    def get_data(self):
        return self.data
    def clear_data(self):
        self.data = []
        self.db_info['DB_length'] = 0
        return



router = APIRouter()

# @router.on_event("startup")
# def startup_event():
#     global db
#     filename = "db.json"
#     if os.path.exists(filename):
#         with open('db.json', 'r') as file:
#             data = json.load(file)
#     else:
#         print("db.json not found, creating new db.json")
#         with open('db.json', 'w') as file:
#             json.dump({}, file)
#         data = {}
#     db = DB()
#     #恢复数据库
#     db.data = data
#     return

# @app.on_event("shutdown")
# def shutdown_event():
#     global db
#     with open('db.json', 'w') as file:
#         json.dump(db.data, file)
#     return
class Item(BaseModel):
    name_DB: str
    action_DB: str
    value: dict
@router.post("/database/")
async def use_DB(
    data: Item
    ):
    global db
    db_type_dict = {
        'sorted_list_DB_type': sorted_list_DB_type
    }
    if data.action_DB == "create_DB":
        db_type = db_type_dict.get(data.value["msg"])
        if db_type == None:
            return {"message": "db_type not found"}
        db.create_DB(data.name_DB, db_type)
        return {"message": "create_DB"}
    elif data.action_DB == "remove_DB":
        db.remove_DB(data.name_DB)
        return {"message": "remove_DB"}
    elif data.action_DB == "add_data":
        db.add_data(data.name_DB, data.value['msg'])
        return {"message": "add_data"}
    elif data.action_DB == "remove_data":
        db.remove_data(data.name_DB, data.value['msg'])
        return {"message": "remove_data"}
    elif data.action_DB == "get_data":
        data = db.get_data(data.name_DB)
        return {"message": "get_data", "data": data}
    else:
        return {"message": "action_DB not found"}

