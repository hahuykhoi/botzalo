import google.generativeai as genai
import logging
from zlapi.models import *  # Giả sử bạn đã cài đặt zlapi
import config # Đảm bảo file config.py tồn tại và chứa GEMINI_API_KEY

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thiết lập API key từ config.py
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
except AttributeError:
    logging.error("Biến GEMINI_API_KEY không được tìm thấy trong file config.py")
    raise

# Tạo model và session chat bên ngoài hàm để tái sử dụng
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

chat_session = model.start_chat()


des = {
    'version': "1.0.0",
    'credits': "Hiển",
    'description': "Trò chuyện với AI"
}

def handle_genz_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2:
        # client.sendReaction(message_object, '👀', thread_id, thread_type)
        error_message = Message(text="Vui lòng nhập câu hỏi để trò chuyện cùng AI.")
        client.sendMessage(error_message, thread_id, thread_type,ttl=6000)
        return

    content = " ".join(text[1:])

    try:
        # Sử dụng chat session đã được tạo sẵn
        chat = chat_session.send_message(content)
        gemini_response = chat.text
        #client.sendReaction(message_object, '⏳', thread_id, thread_type)
        if not gemini_response.strip():
            gemini_response = "Genz không có gì để nói."

        message_to_send = Message(text=f"> Genz: {gemini_response}")
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)

    except Exception as e:
        logging.exception(f"Lỗi khi gọi API: {e}")
        # client.sendReaction(message_object, '👀', thread_id, thread_type)
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type,ttl=5000)



def get_cmds():
    return {
        '': handle_genz_command
    }