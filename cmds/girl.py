from zlapi.models import Message
import requests
import os
des = {
    "version": "1.0.2",
    "credits": "Nguyễn Đức Tài",
    "description": "Xoá tin nhắn người dùng",
}

def handle_girl_command(message, message_object, thread_id, thread_type, author_id, client):
    """Gửi ảnh gái ngẫu nhiên kèm theo một câu thơ.
    -quyền hạn: all
    
    """
    handle_girl_command.permission = "all"

    try:
        # Lấy câu thơ từ API
        thinh_url = "https://api.sumiproject.net/text/thinh"
        thinh_response = requests.get(thinh_url)
        thinh_response.raise_for_status()
        thinh_data = thinh_response.json()
        thinh = thinh_data.get('thinh')

        # Lấy ảnh gái từ API
        girl_api_url = "https://api.sumiproject.net/images/girl"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        girl_response = requests.get(girl_api_url, headers=headers)
        girl_response.raise_for_status()
        girl_data = girl_response.json()
        image_url = girl_data['url']

        # Tạo tin nhắn
        sendmess = f"{thinh}"
        message_to_send = Message(text=sendmess)

        # Tải ảnh và gửi
        image_response = requests.get(image_url, headers=headers)
        image_path = 'temp_image.jpeg'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        client.sendLocalImage(
            image_path,
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1200,
            height=1600
        )

        os.remove(image_path)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_cmds():
    return {
        'girl': handle_girl_command
    }