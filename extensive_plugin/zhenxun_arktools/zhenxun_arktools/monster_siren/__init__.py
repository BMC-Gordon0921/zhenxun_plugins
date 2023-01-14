from nonebot import on_command
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .data_source import search_cloud, build_image

__zx_plugin_name__ = "塞壬点歌"
__plugin_usage__ = """
usage：
    指令：
        塞壬点歌 [歌名]
        塞壬歌单
""".strip()
__plugin_des__ = "就是网易云点歌，还可以看塞壬音乐现在已经有的专辑"
__plugin_cmd__ = ["塞壬点歌"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.1
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["塞壬点歌", "塞壬歌单"],
}

pickup = on_command("塞壬点歌")  # 点歌(qq音乐)
show_list = on_command("塞壬歌单")  # 查看歌单


@pickup.handle()
async def _(arg: Message = CommandArg()):
    keyword = arg.extract_plain_text().strip()
    if not keyword:
        keyword = "Synthetech"

    music = await search_cloud(keyword)
    if not music:
        await pickup.finish(f"网易云音乐中未找到歌曲 {keyword}", at_sender=True)
    await pickup.finish(music)


@show_list.handle()
async def _():
    image = await build_image()
    img = MessageSegment.image(image)
    try:
        await show_list.finish(Message(img))
    except ActionFailed as e:
        await show_list.finish(f"图片发送失败：{e}")
