import os
import time
import sys
import tempfile
import logging
import requests  # Thêm thư viện requests để gửi HTTP request
from datetime import datetime

from zlapi.models import Message, ThreadType
from config import is_admin

# Cấu hình ghi log
logging.basicConfig(filename='bot.log', level=logging.INFO)

RESTART_INFO_FILE = "restart_info.txt"
des = {
    "version": "1.0",
    "credits": "Hiển",
    "description": "",
}

def check_and_send_restart_notification(client):
    """Kiểm tra file tạm thời và gửi thông báo sau khi khởi động lại."""
    if os.path.exists(RESTART_INFO_FILE):
        try:
            with open(RESTART_INFO_FILE, "r") as f:
                restart_timestamp_str = f.readline().strip()
                thread_id = int(f.readline().strip())
                thread_type_value = int(f.readline().strip())
                thread_type = ThreadType(thread_type_value)

            restart_timestamp = datetime.strptime(restart_timestamp_str, "%Y-%m-%d %H:%M:%S")
            time_elapsed = datetime.now() - restart_timestamp
            total_seconds = int(time_elapsed.total_seconds())

            client.sendMessage(Message(text=f"Bot đã khởi động lại! Time: {total_seconds} giây"), thread_id, thread_type, ttl=55555)
        except Exception as e:
            print(f"Lỗi khi gửi thông báo khởi động lại: {e}")
        finally:
            os.remove(RESTART_INFO_FILE)

def shutdown_flask_server():
    """Gửi yêu cầu HTTP để tắt Flask server."""
    try:
        response = requests.post("http://localhost:99/shutdown")
        if response.status_code == 200:
            logging.info("Flask server đã được tắt thành công.")
        else:
            logging.error(f"Lỗi khi tắt Flask server: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Lỗi khi gửi yêu cầu tắt Flask server: {e}")

def restart_bot(message, message_object, thread_id, thread_type, author_id, client):
    """Khởi động lại bot.
    -quyền hạn: admin
    """
    restart_bot.permission = "admin"
    if not is_admin(author_id):
        response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return
    
    try:
        # Lưu thời gian khởi động lại
        restart_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(restart_time.encode())
            temp_file_path = temp_file.name
        os.environ['RESTART_TIME'] = temp_file_path

            # Ghi log
        logging.info(f"Bot được khởi động lại bởi {author_id} vào lúc {restart_time}")

            # Ghi thông tin vào file tạm thời
        with open(RESTART_INFO_FILE, "w") as f:
            f.write(f"{restart_time}\n")
            f.write(f"{thread_id}\n")
            f.write(f"{thread_type.value}\n")

        # Gửi phản hồi trước khi khởi động lại
        client.sendMessage(Message(text="Bot đang khởi động lại..."), thread_id, thread_type, ttl=3000)

        # Tắt server Flask trước khi khởi động lại
        shutdown_flask_server()

        # Chờ một chút để tin nhắn được gửi đi
        time.sleep(2)

        # Khởi động lại bot
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        logging.error(f"Lỗi khi khởi động lại bot: {e}")
        client.sendMessage(Message(text="Đã xảy ra lỗi khi khởi động lại bot."), thread_id, thread_type)
    
def get_cmds():
    return {
        "restart": restart_bot
    }