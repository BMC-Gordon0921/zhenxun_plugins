"""每日开放资源关卡"""
import nonebot
from services.log import logger
from nonebot import on_regex
from nonebot_plugin_apscheduler import scheduler
import os

from nonebot.permission import SUPERUSER
from .data_source import get_daily_sources, DAILY_LEVELS_PATH
from .alter import alter_plan

__zx_plugin_name__ = "方舟今日资源"
__plugin_usage__ = """
usage：
    看看方舟今天哪些资源关开放
    指令：
        方舟今日资源
""".strip()
__plugin_superuser_usage__ = """
usage：
    更新今日方舟资源
    指令：
        更新今日方舟资源
""".strip()
__plugin_des__ = "看看方舟今天哪些资源关开放"
__plugin_cmd__ = ["方舟今日资源", "更新方舟今日资源 [_superuser]"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.2
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["方舟今日资源"],
}

material = on_regex(r"方舟今[日|天]*[资源]*[材料]*", priority=5, block=True)
super_cmd = on_regex(r"更新方舟今[日|天]*[资源]*[材料]*", permission=SUPERUSER, priority=1, block=True)


@material.handle()
async def _():
    rst_img = await get_daily_sources()
    if rst_img:
        rst = rst_img
    else:
        result = await alter_plan()
        result = ", ".join(result)
        rst = (
            f"方舟今日资源截图失败！\n请更换至非windows平台部署本插件\n或检查网络连接并稍后重试\n"
            f"今日开放的资源关卡：{result}"
        )
    await material.finish(rst)


@super_cmd.handle()
async def _():
    try:
        await get_daily_sources(is_force=True)
    except Exception as e:
        logger.error(f"方舟每日资源更新失败！{type(e)}: {e}")
        await super_cmd.finish(f"方舟每日资源更新失败！请稍后重试！")
    else:
        await super_cmd.finish(f"方舟每日资源更新完成！")


@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=1,
)
async def _():
    try:
        await get_daily_sources(is_force=True)
    except Exception as e:
        logger.error(f"方舟每日资源更新失败！{type(e)}: {e}")


driver = nonebot.get_driver()
@driver.on_startup
async def _():
    if not os.path.exists(DAILY_LEVELS_PATH):
        os.makedirs(DAILY_LEVELS_PATH)
    await get_daily_sources(is_force=True)
