from zlapi.models import Message, ThreadType
from youtubesearchpython import VideosSearch
des = {
    "version": "1.0.2",
    "credits": "Nguyễn Đức Tài",
    "description": "Lấy id zalo người dùng hoặc id người được tag",
}

def handle_ytb_command(message, message_object, thread_id, thread_type, author_id, client):
    """Tìm kiếm video trên YouTube.
    -quyền hạn: all
    
    """
    handle_ytb_command.permission = "all"

    parts = message.split(' ', 1)
    if len(parts) < 2:
        client.sendMessage(Message(text="Vui lòng nhập từ khóa tìm kiếm."), thread_id, thread_type)
        return

    search_query = parts[1]
    try:
        videosSearch = VideosSearch(search_query, limit=3)
        results = videosSearch.result()['result']

        response_message = "**Kết quả tìm kiếm trên YouTube:**\n\n"
        for i, video in enumerate(results):
            response_message += f"{i+1}. **{video['title']}**\n"
            response_message += f"   - Link: {video['link']}\n"
            response_message += f"   - Thời lượng: {video['duration']}\n"
            response_message += f"   - Kênh: {video['channel']['name']}\n\n"

        client.sendMessage(Message(text=response_message), thread_id, thread_type)

    except Exception as e:
        client.sendMessage(Message(text=f"Lỗi khi tìm kiếm: {e}"), thread_id, thread_type)

def get_cmds():
    return {
        "ytb": handle_ytb_command
    }