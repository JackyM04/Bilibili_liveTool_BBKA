from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import httpx

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源。在生产环境中，您应该指定具体的来源。
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，如 "GET", "POST", "PUT", "DELETE", "OPTIONS"
    allow_headers=["*"],
)

with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

class Item(BaseModel):
    roomid: str

@app.post("/setting/")
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
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12311)