from zlapi.models import Message
import requests
import random
import os

des = {
    "version": "1.0.7",
    "credits": "Nguyễn Đức Tài",
    "description": "Gửi ảnh gái và câu thính",
}


def handle_anhgai_command(
    message, message_object, thread_id, thread_type, author_id, client
):
    try:
        thinh_url = "http://www.hungdev.id.vn/random/thinh?apiKey=12345"
        response = requests.get(thinh_url)
        response.raise_for_status()
        data = response.json()
        thinh = data.get("data", "Không có câu thính")

        sendmess = f"{thinh}"
        message_to_send = Message(text=sendmess)

        image_list_url = "https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listimg.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        response = requests.get(image_list_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if isinstance(json_data, dict) and "url" in json_data:
            image_url = json_data.get("url")
        elif isinstance(json_data, list):
            image_url = random.choice(json_data)
        else:
            raise Exception("Dữ liệu trả về không hợp lệ")

        image_response = requests.get(image_url, headers=headers)
        image_path = "modules/cache/temp_image1.jpeg"
        with open(image_path, "wb") as f:
            f.write(image_response.content)

        if os.path.exists(image_path):
            client.sendLocalImage(
                image_path,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600,
            )

            os.remove(image_path)
        else:
            raise Exception("Không thể lưu ảnh")

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)


def get_cmds():
    return {"anhgai": handle_anhgai_command}
