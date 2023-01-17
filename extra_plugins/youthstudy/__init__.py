from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Event
from .getdata import get_answer
from nonebot.log import logger
from datetime import datetime

__zx_plugin_name__ = "青年大学习"
__plugin_usage__ = """
usage：
    青年大学习
    指令：
        输入：青年大学习/大学习 以获取最新一期的青年大学习答案
""".strip()
__plugin_des__ = "青年大学习"
__plugin_cmd__ = ["大学习", "青年大学习"]
__plugin_version__ = 1.08
__plugin_author__ = "ayanamiblhx"

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["大学习", "青年大学习"],
}

__plugin_block_limit__ = {"rst": "别卷了，别卷了，秋梨膏"}

college_study = on_command('青年大学习', aliases={'大学习'}, priority=5)


@college_study.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        img = await get_answer()
        if img is None:
            await college_study.send("本周暂未更新青年大学习", at_sender=True)
        elif img == "未找到答案":
            await college_study.send("未找到答案", at_sender=True)
        else:
            await college_study.send(MessageSegment.image(img), at_sender=True)
    except Exception as e:
        await college_study.send(f"出错了，错误信息：{e}", at_sender=True)
        logger.error(f"{datetime.now()}: 错误信息：{e}")
