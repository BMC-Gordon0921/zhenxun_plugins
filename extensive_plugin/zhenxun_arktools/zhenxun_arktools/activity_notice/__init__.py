"""剿灭、蚀刻章、合约等活动到期提醒"""
import nonebot
from services.log import logger
from nonebot import on_regex
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import Message
import os

from .data_source import get_activities, ACTIVITY_PATH, IMAGE_PATH

__zx_plugin_name__ = "方舟最新活动"
__plugin_usage__ = """
usage：
    看看方舟的最新活动是什么
    指令：
        方舟最新活动
""".strip()
__plugin_des__ = "看看方舟的最新活动是什么"
__plugin_cmd__ = ["方舟最新活动"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.2
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["方舟最新活动"],
}


latest_activity = on_regex(r'[查看询]*方舟[最]*新+[活动闻]*', priority=5, block=True)


@latest_activity.handle()
async def _():
    rst_msg = await get_activities(is_force=True)
    if isinstance(rst_msg, Message):
        rst = rst_msg
    elif isinstance(rst_msg, str):
        rst = (
            f"方舟最新活动截图失败！\n请更换至非windows平台部署本插件\n或检查网络连接并稍后重试"
            f"最新的活动信息请见链接: {rst_msg}"
        )
    else:
        rst = f"无法获得方舟最新活动信息！请稍后重试"
    await latest_activity.finish(rst)


@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    try:
        await get_activities(is_force=True, is_cover=True)
    except Exception as e:
        logger.error(f"方舟最新活动检查失败！{type(e)}: {e}")


driver = nonebot.get_driver()
@driver.on_startup
async def _():
    if not os.path.exists(ACTIVITY_PATH):
        os.makedirs(ACTIVITY_PATH)
    if not os.path.exists(f"{IMAGE_PATH}/arktools/activities"):
        os.makedirs(f"{IMAGE_PATH}/arktools/activities")
    await get_activities(is_force=True)
