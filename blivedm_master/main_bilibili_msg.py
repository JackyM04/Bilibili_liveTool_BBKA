# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
from typing import *

import aiohttp

import blivedm_master.blivedm as blivedm
import blivedm_master.blivedm.models.web as web_models

import httpx

import json

with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
with open('./router.json', 'r', encoding='utf-8') as f:
    router = json.load(f)
# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    config['room_id']
]

# 这里填一个已登录账号的cookie。不填cookie也可以连接，但是收到弹幕的用户名会打码，UID会变成0
SESSDATA = ''

session: Optional[aiohttp.ClientSession] = None



async def main():
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()

def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)

async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_clients():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))


class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa
    def __init__(self) -> None:
        global router
        self.data = router


    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        print(f'[{client.room_id}] 心跳')

    def _on_danmaku(self: Any, client: blivedm.BLiveClient, message: web_models.DanmakuMessage) -> None:
        fans_send_data = {
            "data":{
            "uname": message.uname,
            "fans_medal_wearing_status": message.medal_level,
            "guard_level": message.privilege_type,
            "msg": message.msg
            }
        }
        print(fans_send_data)
        with httpx.Client() as http_client:
            response = http_client.post(self.data['URL_chart'], json=fans_send_data)
            print(response.text)
        with httpx.Client() as http_client:
            response = http_client.post(self.data['URL_send_danmu_frequency'], json=fans_send_data)
            print(response.text)
        print(f'[{client.room_id}] {message.uname}：{message.msg}')

    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        # fans_send_data = {
        #     "data":{
        #     "uname": message.uname,
        #     "fans_medal_wearing_status": None,
        #     "guard_level": message.guard_level,
        #     "msg": message.gift_name
        #     }
        # }
        # print(fans_send_data)
        # async with httpx.AsyncClient() as http_client:
        #     response = await http_client.post(self.data['URL_chart'], json=fans_send_data)
        #     print(response.text)
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')

    def _on_buy_guard(self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')


if __name__ == '__main__':
    asyncio.run(main())
