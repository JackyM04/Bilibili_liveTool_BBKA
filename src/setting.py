from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
import httpx

router = APIRouter()


with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

class Item(BaseModel):
    roomid: str

@router.post("/setting/")
async def setting(data: Item):
    try:
        room_id = data.roomid
        with open('./config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        config['room_id'] = room_id

        with open('./config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}
    
