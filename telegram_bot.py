import json
import requests

TOKEN = ""
offset = 0
baseURL = "https://api.telegram.org/bot" + TOKEN

while True:
    try:
        resp = requests.get(baseURL + "/getUpdates",
                            params={"timeout": 60, "offset": offset})
    except Exception:
        break
    try:
        updates = json.loads(resp.text)  # deserialize json
    except Exception:
        break
    if updates["ok"] is not True:
        break
    else:
        result = updates["result"]
    for message in result:
        chat_id = message["message"]["chat"]["id"]
        try:
            text = message["message"]["text"]
            photo = "https://ramottamado.dev/assets/images/xmas.jpg"
            payload = {"chat_id": chat_id, "photo": photo, "caption": text}
            try:
                # resp = requests.post(baseURL + "/sendMessage", data=payload)
                resp = requests.post(baseURL + "/sendPhoto", data=payload)
            except Exception:
                break
        except Exception:
            pass
        offset = message["update_id"] + 1
