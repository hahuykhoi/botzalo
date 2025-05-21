import os
from zlapi.models import Message
import importlib

des = {
    "version": "1.0.2",
    "credits": "Nguyễn Đức Tài",
    "description": "Xem toàn bộ lệnh hiện có của bot",
}


def get_all_cmds():
    cmds = {}

    for module_name in os.listdir("cmds"):
        if module_name.endswith(".py") and module_name != "__init__.py":
            module_path = f"cmds.{module_name[:-3]}"
            module = importlib.import_module(module_path)

            if hasattr(module, "get_cmds"):
                module_cmds = module.get_cmds()
                cmds.update(module_cmds)

    command_names = list(cmds.keys())

    return command_names


def handle_menu_command(
    message, message_object, thread_id, thread_type, author_id, client
):

    command_names = get_all_cmds()

    total_cmds = len(command_names)
    numbered_cmds = [f"{i+1}. {name}" for i, name in enumerate(command_names)]
    menu_message = (
        f"Tổng số lệnh bot hiện tại có: {total_cmds} lệnh \nDưới đây là các lệnh hiện có của bot:\n"
        + "\n".join(numbered_cmds)
    )

    message_to_send = Message(text=menu_message)

    client.replyMessage(message_to_send, message_object, thread_id, thread_type)


def get_cmds():
    return {"menu": handle_menu_command}
