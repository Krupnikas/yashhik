import requests
import json

import config


def sendToScreen(video_url):

    # Auth and getting Session_id

    auth_data = {
            'login': config.login, 
            'passwd': config.password
            }

    s = requests.Session()
    s.get("https://passport.yandex.ru/")
    s.post("https://passport.yandex.ru/passport?mode=auth&retpath=https://yandex.ru", data=auth_data)
    
    Session_id = s.cookies["Session_id"]
    
    # Getting x-csrf-token
    token = s.get('https://frontend.vh.yandex.ru/csrf_token').text

    # Detting devices info TODO: device selection here
    devices_online_stats = s.get("https://quasar.yandex.ru/devices_online_stats").text
    devices = json.loads(devices_online_stats)["items"]

    # Preparing request
    headers = {
        "x-csrf-token": token,
    }

    data = {
        "msg": {
            "provider_item_id": video_url
        },
        "device": devices[0]["id"]
    }

    if "https://www.youtube" in video_url:
        data["msg"]["player_id"] = "youtube"

    # Sending command with video to device
    res = s.post("https://yandex.ru/video/station", data=json.dumps(data), headers=headers)

    return res.text
