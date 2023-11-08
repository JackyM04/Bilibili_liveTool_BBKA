import requests
import time
import asyncio
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import json
import random
router = APIRouter()
danmu_list = []
data_lock = asyncio.Lock()


with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ROOM_IDS = config['room_id']

Threshold = config["danmu_send_thershold"]

now = datetime.now()
# 自动发送的弹幕内容
list_text = config["danmu_list"]

class Item(BaseModel):
    data: dict

@router.post("/send_danmu_frequency/")
async def send_danmu_frequency(data: Item):
    data = data.data
    try:
        # 将数据添加到列表
        async with data_lock:
            danmu_list.append(data)
        return {"status": "success", "message": "data added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def eternal_task():
    try:
        while True:
            # 检查是否有新的弹幕
            await asyncio.sleep(Threshold)
            async with data_lock:
                if len(danmu_list) == 0:
                    print("没有新的弹幕")
                    # 没有新的弹幕
                    send()
                    continue
                else:
                    print("有新的弹幕")
                    # 有新的弹幕
                    # 清空弹幕列表
                    danmu_list.clear()
                
    except asyncio.CancelledError:
        print("Background task cancelled")
        raise
            

@router.on_event("startup")
async def start_eternal_task():
    # 创建并启动后台任务
    task = asyncio.create_task(eternal_task())
    # 这里你可以将 task 存储起来，以便以后可以取消它
    print("Background task started")

def send():
    a = 0

    # 发送的间隔时间
    now = datetime.now()
    now = now.strftime('%H:%M:%S')
    
    send_mesg = random.choice(list_text)
    print(send_mesg)
    url = 'https://api.live.bilibili.com/msg/send'
    data = {
        'buble': '0',
        'msg': send_mesg,
        'color':'16777215',
        'mode': '1',
        'fontsize': '25',
        'rnd': '输入你的rnd',
        'roomid': ROOM_IDS,
        'csrf': '输入你的csrf',
        'csrf_token': '输入你的csrf_token',
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'referer': 'https://live.bilibili.com/8669571?from=search&seid=1038534937018518859&spm_id_from=333.337.0.0',
        'origin': 'https://live.bilibili.com',
        'cookie': "输入你的cookie"
    }
    result=requests.post(url=url,data=data,headers=headers)
    print(result.text)
# if __name__=='__main__':
#     send()
 