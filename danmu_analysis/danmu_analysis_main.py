from fastapi import APIRouter, HTTPException
from typing import Dict
from pydantic import BaseModel

router = APIRouter()

danmu_list = []

class Item(BaseModel):
    data: dict

@router.post("/data_chart/")
async def receive_data(data: Item):  
    data = data.data
    try:
        # 将数据添加到列表
        danmu_list.append(data)
        return {"status": "success", "message": "data added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_chart_data/")
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

