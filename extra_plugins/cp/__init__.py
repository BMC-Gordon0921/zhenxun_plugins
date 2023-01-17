# -*- coding: utf-8 -*-
import os
import random

import ujson
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.typing import T_State

__zx_plugin_name__ = "cp小故事"
__plugin_usage__ = """
usage：
    自定义专属cp(分攻受
    指令：
        cp <攻> <受>
        cp [@user] --自己为攻，被@的人为受
        cp [@user] [@user] --第一个人为攻，第二个人为受
""".strip()
__plugin_des__ = "制作专属于你的cp小故事"
__plugin_cmd__ = [
    "cp [攻] [受]",
]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "AkashiCoin"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [
        "cp [攻] [受]",
    ],
}

cp = on_command("cp", priority=5, block=True)

path = os.path.dirname(__file__)


def readInfo(file):
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        return ujson.loads((f.read()).strip())


def getMessage(name_list):
    content = readInfo("content.json")
    content = (
        random.choice(content["data"])
        .replace("<攻>", name_list[0])
        .replace("<受>", name_list[1])
    )
    return content


@cp.handle()
async def _(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    msg = event.get_message()
    msg_text = args.extract_plain_text().strip()
    name_list = [f"{event.user_id}"]
    for msg_seg in msg:
        if msg_seg.type == "at":
            name_list.append(msg_seg.data["qq"])
    num = len(name_list)
    if num > 1:
        if num > 2:
            del name_list[0]
        for i in range(len(name_list)):
            user_name = await bot.get_group_member_info(
                group_id=event.group_id, user_id=name_list[i]
            )
            user_name = (
                user_name["card"] if user_name["card"] else user_name["nickname"]
            )
            name_list[i] = user_name
    else:
        del name_list[0]
        msg_text = msg_text.split()
        for name in msg_text:
            name_list.append(name)
    await cp.send("\n" + getMessage(name_list), at_sender=True)
