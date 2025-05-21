import re
import os
import sys
import json
import time
from zlapi import *
from zlapi.models import *
from dotenv import load_dotenv
load_dotenv()
IMEI = "a48a5615-9f2b-443a-b1fd-de4ea8ed6409-800683566637788f812c9cb58711ba4c"
SESSION_COOKIES = "{"_ga":"GA1.2.1434526048.1742999799","__zi":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8WyaEsWaKHPYtcIwwFVJ5U6V9BWgp8p.1","__zi-legacy":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8WyaEsWaKHPYtcIwwFVJ5U6V9BWgp8p.1","ozi":"2000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjMXe9fFM8yudkMcdKnNZpkVhgAOJ1c7DPAhefD478q.1","zpsid":"fuLd.429049317.13._osMKkAql_u7SItdxhI__fV7pShGZO_AsuUEoTWE-3-kspg_uo9ywegql_u","zpw_sek":"UXvM.429049317.a0.vThAkooYSVJ9P-Fj3Q9nz5U059yEc5F7ND8QW1p40u5yv1YQMEuSn5wQGBXBdqpMKPZBi-tk7d5je-StECfnz0","app.event.zalo.me":"6448239877774608629","_zlang":"vn"}"
API_KEY = ""
SECRET_KEY = ""
PREFIX = "!"
ADMIN = "3779098888042564741"












SETTING_FILE = "data/setting.json"
def write_settings(settings):
    """Ghi toàn bộ nội dung vào file JSON."""
    with open(SETTING_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)
        
def read_settings():
    """Đọc toàn bộ nội dung từ file JSON."""
    if not os.path.exists(SETTING_FILE):  # Kiểm tra xem file có tồn tại không
        # Nếu không tồn tại, tạo file với nội dung mặc định
        write_settings({})  # Ghi vào file một đối tượng JSON rỗng
    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


settings = read_settings()
ADMIN_BOT = settings.get("admin_bot", [])
def is_admin(author_id):
    settings = read_settings()
    ADMIN_BOT = settings.get("admin_bot", [])
    if author_id in ADMIN_BOT:
        return True
    else:
        return False

def handle_bot_admin(bot):
    settings = read_settings()
    ADMIN_BOT = settings.get("admin_bot", [])
    if bot.uid not in ADMIN_BOT:
        admin_bot.append(bot.uid)
        settings["admin_bot"] = ADMIN_BOT
        write_settings(settings)
        print(
            f"Đã thêm 👑{get_user_name_by_id(bot, bot.uid)} 🆔 {bot.uid} cho lần đầu tiên khởi động vào danh sách Admin BOT ✅"
        )

def get_user_name_by_id(bot, author_id):
    try:
        user = bot.fetchUserInfo(author_id).changed_profiles[author_id].displayName
        return user
    except:
        return "Unknown User"

def get_allowed_thread_ids():
    """Lấy danh sách các groupId có giá trị true trong 'welcome'."""
    settings = read_settings()
    welcome_settings = settings.get("welcome", {})
    allowed_thread_ids = [
        thread_id for thread_id, is_enabled in welcome_settings.items() if is_enabled
    ]
    return allowed_thread_ids
