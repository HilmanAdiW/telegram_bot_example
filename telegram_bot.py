import json
import requests

TOKEN = "1114999373:AAG8-ueFU8wUF_NEzMY4lQFGLGIAHMUY0rA"
offset = 0
base_url = "https://api.telegram.org/bot" + TOKEN
channel_id = -1001437534617
user_list = dict()
media_group_dict = dict()


def handle_satu(chat_id):
    reply = "Silahkan berikan komplain tentang data bermasalah"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(base_url + "/sendMessage", json=payload)
    return resp


def handle_dua(chat_id):
    reply = "Silahkan berikan komplain tentang dashboard error"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(base_url + "/sendMessage", json=payload)
    return resp


def handle_tiga(chat_id):
    reply = "Oh gitu, jadi saya bangsat?"
    payload = {
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": {"remove_keyboard": True, "selective": True},
    }
    resp = requests.post(base_url + "/sendMessage", json=payload)
    return resp


def handle_komplain(chat_id, file_id, first_name, last_name, jenis_komplain, text, jenis_message):
    if jenis_message == "text":
        forwarded_text = f"From: {first_name} {last_name}\n\nJenis komplain: {jenis_komplain}\n\nKomplain: {text}"
        payload_channel = {
            "chat_id": channel_id,
            "text": forwarded_text,
        }
        resp_channel = requests.post(base_url + "/sendMessage", data=payload_channel)
        payload = {
            "chat_id": chat_id,
            "text": "anda telah memberikan komplain. kthxbye.",
        }
        resp = requests.post(base_url + "/sendMessage", data=payload)
        return resp_channel, resp
    elif jenis_message == "foto":
        resp = None
        if text is not None:
            forwarded_text = f"From: {first_name} {last_name}\n\nJenis komplain: {jenis_komplain}\n\nKomplain: {text}"
        else:
            forwarded_text = ""
        payload_channel = {
            "chat_id": channel_id,
            "photo": file_id,
            "caption": forwarded_text
        }
        resp_channel = requests.post(base_url + "/sendPhoto", json=payload_channel)
        payload = {
            "chat_id": chat_id,
            "text": "anda telah memberikan komplain. kthxbye.",
        }
        if text is not None:
            resp = requests.post(base_url + "/sendMessage", data=payload)
        return resp_channel, resp
    else:
        payload = {
            "chat_id": chat_id,
            "text": "format file belum disupport",
        }
        resp = requests.post(base_url + "/sendMessage", data=payload)
        return None, resp


while True:
    try:
        resp = requests.get(
            base_url + "/getUpdates", params={"timeout": 60, "offset": offset}
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
        if "message" in message:
            from_id = message["message"]["from"]["id"]
            chat_id = message["message"]["chat"]["id"]
            try:
                text = message["message"]["text"]
                print(str(from_id) + ": " + text)
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
                                "reply_markup": {
                                    "keyboard": pilihan,
                                    "selective": True,
                                },
                            }
                            resp = requests.post(
                                base_url + "/sendMessage", json=payload
                            )
                            user_list[from_id, chat_id] = None
                        else:
                            payload = {
                                "chat_id": chat_id,
                                "text": "Ketik /start untuk memulai komplain!",
                            }
                            resp = requests.post(
                                base_url + "/sendMessage", data=payload
                            )
                except Exception as e:
                    print(e)
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
                                resp = requests.post(
                                    base_url + "/sendMessage", json=payload
                                )
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
                                resp = requests.post(
                                    base_url + "/sendMessage", json=payload
                                )
                        else:
                            jenis_komplain = user_list[(from_id, chat_id)]
                            first_name = message["message"]["chat"]["first_name"]
                            if "last_name" in message["message"]["chat"]:
                                last_name = message["message"]["chat"]["last_name"]
                            else:
                                last_name = ""
                            print(
                                f"Komplain dari {first_name} {last_name} berjenis {jenis_komplain}. Isinya {text}"
                            )
                            resp_channel, resp = handle_komplain(
                                chat_id=chat_id,
                                file_id=None,
                                first_name=first_name,
                                last_name=last_name,
                                jenis_komplain=jenis_komplain,
                                text=text,
                                jenis_message="text",
                            )
                            user_list.pop((from_id, chat_id), None)
                    else:
                        payload = {"chat_id": chat_id, "text": "anda belum /start"}
                        resp = requests.post(
                            base_url + "/sendMessage", data=payload
                        )
            except Exception:
                jenis_message = None
                file_id = None
                text = ""
                first_name = message["message"]["chat"]["first_name"]
                if "last_name" in message["message"]["chat"]:
                    last_name = message["message"]["chat"]["last_name"]
                else:
                    last_name = ""
                if (from_id, chat_id) in user_list:
                    if user_list[(from_id, chat_id)] is not None:
                        jenis_komplain = user_list[(from_id, chat_id)]
                        if ("photo" in message["message"]) or ("video" in message["message"]):
                            user_list.pop((from_id, chat_id), None)
                            if "caption" in message["message"]:
                                text = message["message"]["caption"]
                            if "photo" in message["message"]:
                                jenis_message = "foto"
                                file_id = message["message"]["photo"][-1]["file_id"]
                            else:
                                jenis_message = "video"
                                file_id = message["message"]["video"]["file_id"]
                            if "media_group_id" in message["message"]:
                                media_group_dict[chat_id] = message["message"]["media_group_id"]
                            resp_channel, resp = handle_komplain(
                                chat_id=chat_id,
                                file_id=file_id,
                                first_name=first_name,
                                last_name=last_name,
                                jenis_komplain=jenis_komplain,
                                text=text,
                                jenis_message=jenis_message,
                            )
                            print(
                                f"Komplain dari {first_name} {last_name} berjenis {jenis_komplain}. Isinya {text}"
                            )
                elif "media_group_id" in message["message"]:
                    if chat_id in media_group_dict:
                        if media_group_dict[chat_id] == message["message"]["media_group_id"]:
                            text = None
                            if "photo" in message["message"]:
                                jenis_message = "foto"
                                file_id = message["message"]["photo"][-1]["file_id"]
                            else:
                                jenis_message = "video"
                                file_id = message["message"]["video"]["file_id"]
                        resp_channel, resp = handle_komplain(
                            chat_id=chat_id,
                            file_id=file_id,
                            first_name=first_name,
                            last_name=last_name,
                            jenis_komplain=jenis_komplain,
                            text=text,
                            jenis_message=jenis_message,
                        )
                        print(
                            f"Komplain dari {first_name} {last_name} berjenis {jenis_komplain}. Isinya {text}"
                        )
                    else:
                        payload = {"chat_id": chat_id, "text": "Terjadi error, coba lagi"}
                        resp = requests.post(base_url + "/sendMessage", data=payload)
                        pass
                else:
                    payload = {"chat_id": chat_id, "text": "Terjadi error, coba lagi"}
                    resp = requests.post(base_url + "/sendMessage", data=payload)
        else:
            pass
        offset = message["update_id"] + 1
