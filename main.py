import threading
from fastapi import FastAPI
#跨域处理
from fastapi.middleware.cors import CORSMiddleware
from danmu_analysis.danmu_analysis_main import router as danmu_analysis_router
from DB.DB_main import router as DB_router
from src.setting import router as setting_router
from danmu_auto_send.main import router as danmu_auto_send_router
from blivedm_master.main_bilibili_msg import main as blivedm_main

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(danmu_analysis_router)
# app.include_router(DB_router)
app.include_router(setting_router)
app.include_router(danmu_auto_send_router)




if __name__ == "__main__":

    import uvicorn
    import asyncio
    asyncio.get_event_loop().create_task(blivedm_main())
    
    def run():
        uvicorn.run(app, host="0.0.0.0", port=12308)

    t = threading.Thread(target=run)
    t.start()
    asyncio.get_event_loop().run_forever()
