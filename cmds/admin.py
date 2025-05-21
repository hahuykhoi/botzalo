from zlapi.models import Message, ThreadType
import json
from config import *
settings = read_settings()
des = {
    "version": "1.0",
    "credits": "Hiển",
    "description": "",
}

def save_admin_bot():
    """Hàm lưu danh sách ADMIN_BOT vào file config.json"""
    settings['admin_bot'] = ADMIN_BOT
    write_settings(settings)
    print("Đã lưu danh sách admin vào file config.json")

def admin_command(message, message_object, thread_id, thread_type, author_id, client):
    """Quản lý danh sách admin bot.

    Permission: admin
    """
    if not is_admin(author_id):
        print(f'{ADMIN_BOT}')
        response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    parts = message.split()
    if len(parts) < 2:
        client.sendMessage(Message(text="Lệnh không hợp lệ. Sử dụng: !admin [list/add/remove]"), thread_id, thread_type)
        return

    action = parts[1].lower()
    if action == "list":
        admin_list = "\n".join([f"- {uid} ({client.fetchUserInfo(uid).changed_profiles[uid].displayName})" for uid in ADMIN_BOT])
        client.sendMessage(Message(text=f"Danh sách admin bot:\n{admin_list}"), thread_id, thread_type)

    elif action in ["add", "remove"]:
        mentions = message_object.get("mentions", [])
        if not mentions:
            client.sendMessage(Message(text="Vui lòng nhắc đến người dùng cần thêm/xóa."), thread_id, thread_type)
            return

        try:
            user_id = mentions[0]["uid"]
            if action == "add":
                if user_id not in ADMIN_BOT:
                    ADMIN_BOT.append(user_id)
                    client.sendMessage(Message(text=f"Đã thêm <{user_id}> vào danh sách admin bot."), thread_id, thread_type)
                    save_admin_bot()  # Lưu thay đổi vào file
                else:
                    client.sendMessage(Message(text=f"<{user_id}> đã có trong danh sách admin bot."), thread_id, thread_type)
            elif action == "remove":
                if user_id in ADMIN_BOT:
                    ADMIN_BOT.remove(user_id)
                    client.sendMessage(Message(text=f"Đã xóa <{user_id}> khỏi danh sách admin bot."), thread_id, thread_type)
                    save_admin_bot()  # Lưu thay đổi vào file
                else:
                    client.sendMessage(Message(text=f"<{user_id}> không có trong danh sách admin bot."), thread_id, thread_type)

        except Exception as e:
            client.sendMessage(Message(text=f"Lỗi: {e}"), thread_id, thread_type)
    else:
        client.sendMessage(Message(text="Lệnh không hợp lệ. Sử dụng: !admin [list/add/remove]"), thread_id, thread_type)

def get_cmds():
    return {
        "admin": admin_command
    }