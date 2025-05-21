import random
import time
from zlapi.models import Message, ThreadType
from config import *
des = {
    "version": "1.0",
    "credits": "Hiển",
    "description": "",
}

def get_user_name(client, user_id):
    """Lấy tên người dùng từ uid."""
    try:
        user_info = client.fetchUserInfo(user_id)
        return user_info.changed_profiles[str(user_id)].displayName
    except Exception as e:
        print(f"Lỗi khi lấy tên người dùng: {e}")
        return None

def var_spam(message, message_object, thread_id, thread_type, author_id, client):
    """var không ngán ai bao giờ.
    -quyền hạn: admin
    
    
    """
    var_spam.permission = "admin"

    if author_id not in ADMIN_BOT:
        client.sendMessage(Message(text="Bạn không có quyền sử dụng lệnh này."), thread_id, thread_type)
        return

    mentions = message_object.get("mentions", [])
    if not mentions:
        client.sendMessage(Message(text="Vui lòng nhắc đến người dùng."), thread_id, thread_type)
        return

    mentioned_user_id = mentions[0]["uid"]

    try:
        with open("data/var.txt", "r", encoding="utf-8") as f:
            messages = f.read().splitlines()

        if messages:
            while True:
                # Lấy mentioned_user_name từ uid trong mỗi vòng lặp
                mentioned_user_name = get_user_name(client, mentioned_user_id)

                msg = random.choice(messages)
                client.sendMessage(Message(text=f"{msg} {mentioned_user_name}"), thread_id, thread_type)
                time.sleep(random.uniform(1, 3))

                # Lắng nghe lệnh !var off từ admin
                last_messages = client.getLastMsgs()
                if thread_type == ThreadType.USER:
                    recent_messages = last_messages.msgs
                else:
                    recent_messages = last_messages.groupMsgs

                for recent_message in recent_messages:
                    if recent_message['uidFrom'] in ADMIN_BOT and recent_message['content'] == f"{PREFIX}var off":
                        client.sendMessage(Message(text=f"Lần này tha cho mày đó {mentioned_user_name}"), thread_id, thread_type)
                        return  # Thoát khỏi vòng lặp spam
        else:
            client.sendMessage(Message(text="File var.txt trống."), thread_id, thread_type)
    except Exception as e:
        client.sendMessage(Message(text=f"Lỗi khi spam: {e}"), thread_id, thread_type)

def get_cmds():
    return {
        "var": var_spam
    }