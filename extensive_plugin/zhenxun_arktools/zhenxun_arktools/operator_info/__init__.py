"""获取干员信息"""
from nonebot import on_command
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .._exceptions import OperatorNotExistException
from .data_source import *

__zx_plugin_name__ = "方舟干员信息"
__plugin_usage__ = """
usage：
    查看干员的技能升级材料、技能专精材料、精英化材料
    指令：
        干员 [干员中文名称]
""".strip()
__plugin_des__ = "查看干员的技能升级材料、技能专精材料、精英化材料"
__plugin_cmd__ = ["干员", "方舟干员", "明日方舟干员"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.1
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["干员", "方舟干员", "明日方舟干员"],
}

query_operator = on_command("干员", aliases={"方舟干员", "明日方舟干员"})


@query_operator.handle()
async def _(arg: Message = CommandArg()):
    try:
        name = arg.extract_plain_text().strip()
        try:
            op = OperatorInfo(name)
        except OperatorNotExistException as e:
            await query_operator.finish(e.msg, at_sender=True)
        build = BuildOperatorImage(op)
        img = build.build_whole_image()

        img = MessageSegment.image(img)
        await query_operator.finish(Message(img))
    except ActionFailed as e:
        await query_operator.finish(f"图片发送失败！{e}", at_sender=True)