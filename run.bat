@echo off
cd /d %~dp0
call conda activate BtVRC
start python .\danmu_analysis\main.py
start python .\blivedm-master\main_bilibili_msg.py
cd .\fronend_code

start npm install
npm start