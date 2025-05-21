from zlapi.models import Message, Mention, MultiMention

des = {
    "version": "1.0",
    "credits": "Hiển",
    "description": "",
}

def handle_uid_command(message, message_object, thread_id, thread_type, author_id, client):
    """Trả về uid của người được nhắc đến, nếu không có ai được nhắc đến thì trả về uid của người gửi.
    -quyền hạn: all

    """
    handle_uid_command.permission = "all"
    
    mentions = message_object.get("mentions", [])
    if mentions:
        # Nếu có người được nhắc đến
        try:
            # Lấy uid của người đầu tiên được nhắc đến
            mentioned_user_id = mentions[0]["uid"] 
            response_message = f"{mentioned_user_id}"
        except (IndexError, KeyError) as e:
            response_message = f"Lỗi khi lấy uid của người được nhắc đến: {e}"
    else:
        # Nếu không có ai được nhắc đến
        response_message = f"{author_id}"

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_cmds():
    return {
        "uid": handle_uid_command
    }