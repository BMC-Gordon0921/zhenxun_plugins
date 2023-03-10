from nonebot.rule import T_State
from nonebot import on_message, get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
import re
from .config import Config
from .data_source import get_github_reposity_information


__zx_plugin_name__ = "Github仓库信息卡片"
__plugin_usage__ = """
usage：
    Github 仓库信息卡片
  
""".strip()
__plugin_des__ = "Github仓库信息卡片"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["]"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["Github仓库信息卡片"],
}


global_config = get_driver().config
config = Config(**global_config.dict())
github = on_message(priority=5)


@github.handle()
async def github_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    url = event.get_plaintext()
    if re.match("https://github.com/.*?/.*?", url) != None:
        imageUrl = await get_github_reposity_information(url)
        assert(imageUrl != "获取信息失败")
        await github.send(Message(f"[CQ:image,file={imageUrl}]"))
        await github.finish(Message(f"[CQ:image,file=https://image.thum.io/get/width/1280/crop/1440/viewportWidth/1280/png/noanimate/{url}]"))
