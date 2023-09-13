@echo off
cd /d %~dp0
call conda activate BtVRC
start python main.py
cd ./bika_frontend
npm start