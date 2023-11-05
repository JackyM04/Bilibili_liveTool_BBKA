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

Threshold = 15

now = datetime.now()
# 自动发送的弹幕内容
list_text = ["‘测试’免费人气票什么的拜托各位送一送！",
             "‘测试’关注咔比大王 咔，老板大气 咔",
             "‘测试’欢迎大家进入直播间，这是测试",
             ]

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
        'rnd': '1699185762',
        'roomid': ROOM_IDS,
        'csrf': '8ee39866fab5e88c9edda82644b36546',
        'csrf_token': '8ee39866fab5e88c9edda82644b36546',
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'referer': 'https://live.bilibili.com/8669571?from=search&seid=1038534937018518859&spm_id_from=333.337.0.0',
        'origin': 'https://live.bilibili.com',
        'cookie': "buvid3=7D5C990E-273E-2FC6-C074-42A0AE600BEB27305infoc; b_nut=1669110027; i-wanna-go-back=-1; _uuid=624256102-52E9-B787-10D22-DAD996A108105D26501infoc; buvid4=A17D5F52-AEE1-6F4D-C71C-5188F876EC5D31482-022071401-hsC6fRrGrTUQxQL2gVSh0A%3D%3D; buvid_fp_plain=undefined; nostalgia_conf=-1; rpdid=|(umR~luuumJ0J'uYYmuu|R|l; LIVE_BUVID=AUTO6616691264158302; hit-dyn-v2=1; blackside_state=0; b_ut=5; CURRENT_BLACKGAP=0; hit-new-style-dyn=1; CURRENT_PID=e933a510-c89d-11ed-a55a-779d7f10745c; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; SESSDATA=a6328ac9%2C1707740195%2Cf8c05%2A827anwP4SKEHYEgZdlaeHJUGJxpdEBRvn1-zphVJDDX2ogcakZ5MD99gSab977WWpVv4R75gAASQA; bili_jct=8ee39866fab5e88c9edda82644b36546; DedeUserID=180413373; DedeUserID__ckMd5=0d38437489d60a69; sid=8b95ah2u; _ga=GA1.1.1349167444.1695543557; _ga_HE7QWR90TV=GS1.1.1695543557.1.1.1695543627.0.0.0; header_theme_version=CLOSE; enable_web_push=DISABLE; CURRENT_QUALITY=120; fingerprint=f1633472f79339f9acba452b2526e7d3; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1698578079,1698669714,1698928611,1699018979; PVID=1; buvid_fp=7D5C990E-273E-2FC6-C074-42A0AE600BEB27305infoc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTkzMDU0NTIsImlhdCI6MTY5OTA0NjE5MiwicGx0IjotMX0.cZqOJ7simkLjdRLIl6LWC2tI2WlEnOT5CP0gUiiMKLs; bili_ticket_expires=1699305392; bp_video_offset_180413373=860454358233382919; innersign=0; home_feed_column=4; browser_resolution=1078-751"
    }
    result=requests.post(url=url,data=data,headers=headers)
    print(result.text)
# if __name__=='__main__':
#     send()
 