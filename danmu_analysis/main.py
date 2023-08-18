from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源。在生产环境中，您应该指定具体的来源。
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，如 "GET", "POST", "PUT", "DELETE", "OPTIONS"
    allow_headers=["*"],
)

danmu_list = []


class Item(BaseModel):
    data: dict

@app.post("/data_chart/")
async def receive_data(data: Item):  
    data = data.data
    try:
        # 将数据添加到列表
        danmu_list.append(data)
        return {"status": "success", "message": "data added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_chart_data/")
async def get_chart_data():
    name_count = {}
    for item in danmu_list:
        name = item['uname']
        if name in name_count:
            name_count[name] += 1
        else:
            name_count[name] = 1

    sorted_names = sorted(name_count.items(), key=lambda x: x[1], reverse=True)  
    names, counts = zip(*sorted_names)

    return {"labels": names, "counts": counts}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12310)
