from zlapi.models import Message
import requests
import urllib.parse

des = {
    "version": "1.9.2",
    "credits": "Nguyễn Đức Tài",
    "description": "trò chuyện với simi",
}


def handle_sim_command(
    message, message_object, thread_id, thread_type, author_id, client
):
    text = message.split()

    if len(text) < 2:
        error_message = Message(text="Vui lòng nhập câu hỏi để trò chuyện cùng simi.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    content = " ".join(text[1:])
    encoded_text = urllib.parse.quote(content, safe="")

    try:
        sim_url = f"https://freeapi.mxhgiare.net/v2/simi/get?ask={encoded_text}"
        response = requests.get(sim_url)
        response.raise_for_status()

        data = response.json()
        simi = data.get("msg", "Không có phản hồi từ Simi.")
        message_to_send = Message(text=f"> Sim: {simi}")

        client.replyMessage(message_to_send, message_object, thread_id, thread_type)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except KeyError as e:
        error_message = Message(text=f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi không xác định: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)


def get_mitaizl():
    return {"sim": handle_sim_command}
