import os
import importlib
import sys
import random
import json
from zlapi.models import Message
from config import *
from logging_utils import Logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logger = Logging()


class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.cmds = self.load_cmds()
        self.auto_cmds = self.load_auto_cmds()
        self.admin_id = ADMIN
        self.adminon = self.load_admin_mode()

        if PREFIX == "":
            logger.prefixcmd("Prefix hiện tại của bot là 'NO PREFIX'")
        else:
            logger.prefixcmd(f"Prefix hiện tại của bot là '{PREFIX}'")

    def load_admin_mode(self):
        try:
            with open("data/admindata.json", "r") as f:
                data = json.load(f)
                return data.get("adminon", False)
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            return False

    def save_admin_mode(self):
        with open("data/admindata.json", "w") as f:
            json.dump({"adminon": self.adminon}, f)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb_color):
        return "{:02x}{:02x}{:02x}".format(*rgb_color)

    def generate_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def generate_gradient_colors(self, length, num_colors=5):
        random_colors = [self.generate_random_color() for _ in range(num_colors)]
        rgb_colors = [self.hex_to_rgb(color) for color in random_colors]

        colors = []
        for j in range(num_colors - 1):
            start_rgb = rgb_colors[j]
            end_rgb = rgb_colors[j + 1]
            segment_length = length // (num_colors - 1)

            for i in range(segment_length):
                interpolated_color = (
                    int(
                        start_rgb[0]
                        + (end_rgb[0] - start_rgb[0]) * i / (segment_length - 1)
                    ),
                    int(
                        start_rgb[1]
                        + (end_rgb[1] - start_rgb[1]) * i / (segment_length - 1)
                    ),
                    int(
                        start_rgb[2]
                        + (end_rgb[2] - start_rgb[2]) * i / (segment_length - 1)
                    ),
                )
                colors.append(self.rgb_to_hex(interpolated_color))

        return colors

    def create_rainbow_params(self, text, size=20):
        styles = []
        colors = self.generate_gradient_colors(len(text), num_colors=5)

        for i, color in enumerate(colors):
            styles.append({"start": i, "len": 1, "st": f"c_{color}"})

        params = {"styles": styles, "ver": 0}
        return json.dumps(params)

    def sendMessageColor(self, error_message, thread_id, thread_type, ttl):
        stype = self.create_rainbow_params(error_message)
        mes = Message(text=error_message, style=stype)
        self.client.send(mes, thread_id, thread_type, ttl=ttl)

    def replyMessageColor(self, error_message, message_object, thread_id, thread_type, ttl):
        stype = self.create_rainbow_params(error_message)
        mes = Message(text=error_message, style=stype)
        self.client.replyMessage(
            mes, message_object, thread_id=thread_id, thread_type=thread_type, ttl=ttl)

    def load_cmds(self):
        cmds = {}
        modules_path = "cmds"
        success_count = 0
        failed_count = 0
        success_cmds = []
        failed_cmds = []

        for filename in os.listdir(modules_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{modules_path}.{module_name}")

                    if hasattr(module, "get_cmds"):
                        if hasattr(module, "des"):
                            des = getattr(module, "des")
                            if all(
                                key in des
                                for key in ["version", "credits", "description"]
                            ):
                                cmds.update(module.get_cmds())
                                success_count += 1
                                success_cmds.append(module_name)
                            else:
                                raise ImportError(
                                    f"Lỗi không thể tìm thấy thông tin của lệnh: {module_name}"
                                )
                        else:
                            raise ImportError(f"Lệnh {module_name} không có thông tin")
                    else:
                        raise ImportError(f"Module {module_name} không có hàm gọi lệnh")
                except Exception as e:
                    logger.error(f"Không thể load được module: {module_name}. Lỗi: {e}")
                    failed_count += 1
                    failed_cmds.append(module_name)

        if success_count > 0:
            logger.success(
                f"Đã load thành công {success_count} lệnh: {', '.join(success_cmds)}"
            )
        if failed_count > 0:
            logger.warning(
                f"Không thể load được {failed_count} lệnh: {', '.join(failed_cmds)}"
            )

        return cmds

    def load_auto_cmds(self):
        auto_cmds = {}
        auto_modules_path = "cmds.auto"
        success_count = 0
        failed_count = 0
        success_auto_cmds = []
        failed_auto_cmds = []

        for filename in os.listdir("cmds/auto"):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(
                        f"{auto_modules_path}.{module_name}"
                    )

                    if hasattr(module, "get_cmds"):
                        if hasattr(module, "des"):
                            des = getattr(module, "des")
                            if all(
                                key in des
                                for key in ["version", "credits", "description"]
                            ):
                                auto_cmds.update(module.get_cmds())
                                success_count += 1
                                success_auto_cmds.append(module_name)
                            else:
                                raise ImportError(
                                    f"Module {module_name} thiếu các thông tin cần thiết"
                                )
                        else:
                            raise ImportError(f"Lệnh {module_name} không có thông tin")
                    else:
                        raise ImportError(f"Module {module_name} không có hàm gọi lệnh")
                except Exception as e:
                    logger.error(f"Không thể load được module: {module_name}. Lỗi: {e}")
                    failed_count += 1
                    failed_auto_cmds.append(module_name)

        if success_count > 0:
            logger.success(
                f"Đã load thành công {success_count} lệnh auto: {', '.join(success_auto_cmds)}"
            )
        if failed_count > 0:
            logger.warning(
                f"Không thể load được {failed_count} lệnh auto: {', '.join(failed_auto_cmds)}"
            )

        return auto_cmds

    def toggle_admin_mode(
        self, message, message_object, thread_id, thread_type, author_id
    ):
        if author_id == self.admin_id:
            if "on" in message.lower():
                self.adminon = True
                self.save_admin_mode()
                self.replyMessageColor(
                    "Chế độ admin đã được bật.", message_object, thread_id, thread_type, ttl=60000
                )
            elif "off" in message.lower():
                self.adminon = False
                self.save_admin_mode()
                self.replyMessageColor(
                    "Chế độ admin đã được tắt.", message_object, thread_id, thread_type
                )
            else:
                self.replyMessageColor(
                    "Vui lòng sử dụng lệnh: adminmode on/off.",
                    message_object,
                    thread_id,
                    thread_type,ttl=60000
                )
        else:
            self.replyMessageColor(
                "Bạn không có quyền bật/tắt chế độ admin.",
                message_object,
                thread_id,
                thread_type,ttl=60000
            )

    def handle_command(
        self, message, author_id, message_object, thread_id, thread_type
    ):
        if message.startswith(PREFIX + "adminmode"):
            self.toggle_admin_mode(
                message, message_object, thread_id, thread_type, author_id
            )
            return

        auto_command_handler = self.auto_cmds.get(message.lower())
        if auto_command_handler:
            auto_command_handler(
                message, message_object, thread_id, thread_type, author_id, self.client
            )
            return

        if not message.startswith(PREFIX):
            return

        if self.adminon and author_id != self.admin_id:
            error_message = (
                "Chế độ admin đang bật, chỉ có admin mới có thể sử dụng lệnh."
            )
            self.replyMessageColor(
                error_message, message_object, thread_id, thread_type, ttl=60000
            )
            return

        command_name = message[len(PREFIX) :].split(" ")[0].lower()
        command_handler = self.cmds.get(command_name)

        if command_handler:
            command_handler(
                message, message_object, thread_id, thread_type, author_id, self.client
            )
        else:
            error_message = f"Không tìm thấy lệnh '{command_name}'. Hãy dùng {PREFIX}menu để biết các lệnh có trên hệ thống."
            self.replyMessageColor(
                error_message, message_object, thread_id, thread_type, ttl= 60000
            )
