from config import *
from soiz import CommandHandler
from zlapi import ZaloAPI
from colorama import Fore, Style, init
from cmds.auto.eventgroup import *
from cmds.restart import *

init(autoreset=True)


class Client(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(
            api_key, secret_key, imei=imei, session_cookies=session_cookies
        )
        self.command_handler = CommandHandler(self)
        #wl
        self.group_info_cache = {} 
        all_group = self.fetchAllGroups()
        allowed_thread_ids = list(all_group.gridVerMap.keys())
       
    def onLoggedIn(self, phone=None):
        """Hàm này được gọi khi client đăng nhập thành công."""
        self.uid = self._state.user_id
        logger.login_success(f"UID: {self.uid}")
        check_and_send_restart_notification(self)
        
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        sender_name = self.fetchUserInfo(author_id).changed_profiles[author_id].displayName
        current_time = datetime.now().strftime("%H:%M:%S")
        sender_id= author_id
        if sender_id != self.uid:
            if thread_type== ThreadType.USER:
                print(f"Tin nhắn riêng | {sender_name}: {message}")
            else:
                group_name = self.fetchGroupInfo(thread_id).gridInfoMap[str(thread_id)]['name']
                print(f"Tin nhắn nhóm | {group_name} | {sender_name}: {message}")

        try:
            if isinstance(message, str):
                self.command_handler.handle_command(
                    message, author_id, message_object, thread_id, thread_type
                )
        except Exception as e:
            logger.error(f"main.onMessage: {e}")

    def onEvent(self, event_data, event_type):
        """Xử lý sự kiện nhóm."""
        handle_event(event_data, event_type, self)
        

if __name__ == "__main__":
    client = Client( "</>", "</>", IMEI, SESSION_COOKIES)
    client.listen(thread=True)
