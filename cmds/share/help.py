import os
from zlapi.models import Message
import importlib

des = {
    "version": "1.0.2",
    "credits": "Nguyễn Đức Tài",
    "description": "Lệnh này cung cấp thông tin chi tiết về các lệnh khác.",
}


def get_all_mitaizl_with_info():
    mitaizl_info = {}

    for module_name in os.listdir("modules"):
        if module_name.endswith(".py") and module_name != "__init__.py":
            module_path = f"modules.{module_name[:-3]}"
            module = importlib.import_module(module_path)

            if hasattr(module, "des"):
                des = getattr(module, "des")
                version = des.get("version", "Chưa có thông tin")
                credits = des.get("credits", "Chưa có thông tin")
                description = des.get("description", "Chưa có thông tin")
                mitaizl_info[module_name[:-3]] = (version, credits, description)

    return mitaizl_info


def handle_help_command(
    message, message_object, thread_id, thread_type, author_id, client
):
    command_parts = message.split()

    mitaizl_info = get_all_mitaizl_with_info()

    if len(command_parts) > 1:
        requested_command = command_parts[1].lower()

        if requested_command in mitaizl_info:
            version, credits, description = mitaizl_info[requested_command]
            single_command_help = f"• Tên lệnh: {requested_command}\n• Phiên bản: {version}\n• Credits: {credits}\n• Mô tả: {description}"
            all_commands_help = None
        else:
            single_command_help = (
                f"Không tìm thấy lệnh '{requested_command}' trong hệ thống."
            )
            all_commands_help = None

    else:
        total_mitaizl = len(mitaizl_info)

        help_message_lines = [f"Tổng số lệnh bot hiện tại: {total_mitaizl} lệnh"]
        for i, (name, (version, credits, description)) in enumerate(
            mitaizl_info.items(), 1
        ):
            help_message_lines.append(
                f"{i}:\n• Tên lệnh: {name}\n• Phiên bản: {version}\n• Credits: {credits}\n• Mô tả: {description}\n"
            )

        all_commands_help = "\n".join(help_message_lines)
        single_command_help = None

    if single_command_help:
        message_to_send = Message(text=single_command_help)
    else:
        message_to_send = Message(text=all_commands_help)

    client.replyMessage(message_to_send, message_object, thread_id, thread_type)


def get_mitaizl():
    return {"help": handle_help_command}
