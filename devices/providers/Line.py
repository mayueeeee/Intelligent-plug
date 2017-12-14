import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from os import environ
load_dotenv(find_dotenv())

def send(message,img_full=None,img_thumb=None):    
    headers = {"authorization":"Bearer "+environ.get("LINE_TOKEN")}
    payload = {
        'message':message,
        'imageFullsize':img_full,
        'imageThumbnail':img_thumb
    }
    r = requests.post('https://notify-api.line.me/api/notify',headers=headers,data=payload)
    # print(r.text)

