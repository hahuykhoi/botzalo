import os
import importlib
from zlapi.models import Message

des = {
    "version": "1.0.2",
    "credits": "Nguyễn Đức Tài",
    "description": "Load, loadall, unload lệnh",
}

loaded_cmds = {}


def get_all_cmds():
    cmds = {}
    for module_name in os.listdir("cmds"):
        if module_name.endswith(".py") and module_name != "__init__.py":
            module_path = f"cmds.{module_name[:-3]}"
            try:
                module = importlib.import_module(module_path)

                if hasattr(module, "get_cmds"):
                    module_cmds = module.get_cmds()
                    cmds.update(module_cmds)
            except Exception as e:
                print(f"Lỗi khi load module {module_name}: {e}")
    return cmds


def handle_cmd_command(
    message, message_object, thread_id, thread_type, author_id, client
):
    content = message.strip().split()

    if len(content) < 2:
        error_message = "Bạn cần cung cấp lệnh (load, unload, loadall, unloadall)."
        client.replyMessage(
            Message(text=error_message), message_object, thread_id, thread_type
        )
        return

    action = content[1].lower()

    if action == "load" and len(content) == 3:
        command_name = content[2]
        all_cmds = get_all_cmds()
        if command_name in all_cmds:
            try:
                loaded_cmds[command_name] = all_cmds[command_name]
                success_message = f"Load thành công lệnh '{command_name}'."
                client.replyMessage(
                    Message(text=success_message),
                    message_object,
                    thread_id,
                    thread_type,
                )
            except Exception as e:
                error_message = f"Load lệnh '{command_name}' thất bại: {str(e)}"
                client.replyMessage(
                    Message(text=error_message), message_object, thread_id, thread_type
                )
        else:
            error_message = f"Lệnh '{command_name}' không tồn tại."
            client.replyMessage(
                Message(text=error_message), message_object, thread_id, thread_type
            )

    elif action == "unload" and len(content) == 3:
        command_name = content[2]
        if command_name in loaded_cmds:
            del loaded_cmds[command_name]
            success_message = f"Unload thành công lệnh '{command_name}'."
            client.replyMessage(
                Message(text=success_message), message_object, thread_id, thread_type
            )
        else:
            error_message = f"Lệnh '{command_name}' không được load hoặc không tồn tại."
            client.replyMessage(
                Message(text=error_message), message_object, thread_id, thread_type
            )

    elif action == "loadall":
        all_cmds = get_all_cmds()
        success_count = 0
        error_list = []
        for command_name, command_function in all_cmds.items():
            try:
                loaded_cmds[command_name] = command_function
                success_count += 1
            except Exception as e:
                error_list.append(f"Lệnh '{command_name}' lỗi: {str(e)}")

        success_message = f"Đã load thành công {success_count} lệnh."
        if error_list:
            error_message = "Một số lệnh lỗi:\n" + "\n".join(error_list)
            client.replyMessage(
                Message(text=error_message), message_object, thread_id, thread_type
            )

        client.replyMessage(
            Message(text=success_message), message_object, thread_id, thread_type
        )

    elif action == "unloadall":
        loaded_cmds.clear()
        success_message = "Đã unload thành công toàn bộ lệnh."
        client.replyMessage(
            Message(text=success_message), message_object, thread_id, thread_type
        )

    else:
        error_message = "Cú pháp không đúng hoặc không đủ tham số."
        client.replyMessage(
            Message(text=error_message), message_object, thread_id, thread_type
        )


def get_cmds():
    return {"cmd": handle_cmd_command}
