from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message

from .data_source import check_text, random_text

__zx_plugin_name__ = "枝网查重"
__plugin_usage__ = """
usage：
1.查重 然然，我今天发工资了，发了1300。你肯定觉得我会借14块钱，然后给你打个1314块的sc对不对？不是哦，我一块都不打给你，因为我要打给乃琳捏

2小作文
""".strip()
__plugin_des__ = "功能"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["枝网查重"]
__plugin_author__ = "wq!!!!"

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["枝网查重"],
}

asoulcnki = on_command('asoulcnki', aliases={'枝网查重', '查重'},
                       block=True, priority=5)


@asoulcnki.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        if event.reply:
            reply = event.reply.message.extract_plain_text().strip()
            if reply:
                text = reply

    if not text:
        await asoulcnki.finish()

    if len(text) >= 1000:
        await asoulcnki.finish('文本过长，长度须在10-1000之间')
    elif len(text) <= 10:
        await asoulcnki.finish('文本过短，长度须在10-1000之间')

    msg = await check_text(text)
    if msg:
        await asoulcnki.finish(msg)
    else:
        await asoulcnki.finish('出错了，请稍后再试')


article = on_command('小作文', aliases={'随机小作文', '发病小作文'},
                     block=True, priority=5)


@article.handle()
async def _(msg: Message = CommandArg()):
    keyword = msg.extract_plain_text().strip()

    msg = await random_text(keyword)
    if msg:
        await article.finish(msg)
    else:
        await article.finish('出错了，请稍后再试')
