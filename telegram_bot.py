import json
import pandas as pd
import requests
import os

TOKEN = ""
offset = 0
baseURL = "https://api.telegram.org/bot" + TOKEN

user_list = dict()

data_komplain = pd.DataFrame.from_dict(
    data={"first_name": [], "last_name": [], "jenis_komplain": [], "isi_komplain": []}
)

if "data_komplain.csv" not in os.listdir():
    data_komplain.to_csv("data_komplain.csv", header=True, index=False)


def handle_satu(chat_id):
    reply = "Silahkan berikan komplain tentang data bermasalah"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(baseURL + "/sendMessage", json=payload)
    return resp


def handle_dua(chat_id):
    reply = "Silahkan berikan komplain tentang dashboard error"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(baseURL + "/sendMessage", json=payload)
    return resp


def handle_tiga(chat_id):
    reply = "Oh gitu, jadi saya bangsat?"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(baseURL + "/sendMessage", json=payload)
    return resp


while True:
    try:
        resp = requests.get(
            baseURL + "/getUpdates", params={"timeout": 60, "offset": offset}
        )
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
        from_id = message["message"]["from"]["id"]
        chat_id = message["message"]["chat"]["id"]
        try:
            text = message["message"]["text"]
            print(text)
            try:
                if message["message"]["entities"][0]["type"] == "bot_command":
                    if text == "/start":
                        user_list.pop((from_id, chat_id), None)
                        pilihan = [
                            [{"text": "Data bermasalah"}],
                            [{"text": "Dashboard error"}],
                            [{"text": "Anda bangsat"}],
                            [{"text": "Batalkan"}],
                        ]
                        payload = {
                            "chat_id": chat_id,
                            "text": "Pilih salah satu",
                            "reply_markup": {"keyboard": pilihan, "selective": True,},
                        }
                        resp = requests.post(baseURL + "/sendMessage", json=payload)
                        user_list[from_id, chat_id] = None
                    else:
                        payload = {
                            "chat_id": chat_id,
                            "text": "Ketik /start untuk memulai komplain!",
                        }
                        resp = requests.post(baseURL + "/sendMessage", data=payload)
            except Exception:
                if (from_id, chat_id) in user_list:
                    if user_list[(from_id, chat_id)] is None:
                        if text == "Data bermasalah":
                            resp = handle_satu(chat_id)
                            user_list[(from_id, chat_id)] = text
                        elif text == "Dashboard error":
                            resp = handle_dua(chat_id)
                            user_list[(from_id, chat_id)] = text
                        elif text == "Anda bangsat":
                            resp = handle_tiga(chat_id)
                            user_list[(from_id, chat_id)] = text
                        elif text == "Batalkan":
                            payload = {
                                "chat_id": chat_id,
                                "text": "Anda membatalkan komplain",
                                "reply_markup": {
                                    "remove_keyboard": True,
                                    "selective": True,
                                },
                            }
                            resp = requests.post(baseURL + "/sendMessage", json=payload)
                            user_list.pop((from_id, chat_id), None)
                        else:
                            payload = {
                                "chat_id": chat_id,
                                "text": "Salah pilihan bapacc",
                                "reply_markup": {
                                    "remove_keyboard": True,
                                    "selective": True,
                                },
                            }
                            resp = requests.post(baseURL + "/sendMessage", json=payload)
                    else:
                        jenis_komplain = user_list[(from_id, chat_id)]
                        payload = {
                            "chat_id": chat_id,
                            "text": "anda telah memberikan komplain. kthxbye.",
                        }
                        resp = requests.post(baseURL + "/sendMessage", data=payload)
                        first_name = message["message"]["chat"]["first_name"]
                        if "last_name" in message["message"]["chat"]:
                            last_name = message["message"]["chat"]["last_name"]
                        else:
                            last_name = ""
                        print(
                            f"Komplain dari {first_name} {last_name} berjenis {jenis_komplain}. Isinya {text}"
                        )
                        data_komplain = pd.DataFrame.from_dict(
                            {
                                "first_name": [first_name],
                                "last_name": [last_name],
                                "jenis_komplain": [jenis_komplain],
                                "isi_komplain": [text],
                            }
                        )
                        data_komplain.to_csv(
                            "data_komplain.csv", mode="a", header=False, index=False
                        )
                        user_list.pop((from_id, chat_id), None)
                else:
                    payload = {"chat_id": chat_id, "text": "anda belum /start"}
                    resp = requests.post(baseURL + "/sendMessage", data=payload)
        except Exception:
            payload = {"chat_id": chat_id, "text": "Terjadi error"}
            resp = requests.post(baseURL + "/sendMessage", data=payload)
        offset = message["update_id"] + 1
