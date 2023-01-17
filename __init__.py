import requests,json,urllib3
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

__zx_plugin_name__ = "QQ权重"
__plugin_usage__ = """
usage：
    QQ查权重 权重越低越容易封号，权重低时要多加注意啦
    指令：
        查权重 [QQ号码]
        bot权重/BOT权重  查询BOT的权重
""".strip()
__plugin_des__ = "QQ查权重"
__plugin_cmd__ = ["查权重","bot权重","BOT权重"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "liuli"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查权重","bot权重","BOT权重"],
}


weight = on_command("查权重", priority=5, block=True)
bot = on_command("bot权重", aliases={"BOT权重"}, priority=5, block=True,permission=SUPERUSER)

@weight.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    number = arg.extract_plain_text().strip()
    if number:
        url = f'http://tc.tfkapi.top/API/qqqz.php?type=json&qq={number}'
        response = urllib3.PoolManager().request('GET', url)
        if response==None:
            weight.send("网站维护中，请稍后。") 
        res = json.loads(response.data.decode())
        code = res['code']
        if code!=200:
            await weight.send("查询失败！请重试，或检查QQ号。")
        msg = res['msg']
        qz = res['qz']
        await weight.send(f"您的QQ号码：{number}\n查询状态：{msg}\nQQ权重分：{qz}\n权重越低越容易封号，权重低时要多加注意啦", at_sender=True)
    else:
        number = event.user_id
        url = f'http://tc.tfkapi.top/API/qqqz.php?type=json&qq={number}'
        response = urllib3.PoolManager().request('GET', url)
        if response==None:
            weight.send("网站维护中，请稍后。") 
        res = json.loads(response.data.decode())
        code = res['code']
        if code!=200:
            await weight.send("查询失败！请重试，或检查QQ号。")
        msg = res['msg']
        qz = res['qz']
        await weight.send(f"您的QQ号码：{number}\n查询状态：{msg}\nQQ权重分：{qz}\n权重越低越容易封号，权重低时要多加注意啦", at_sender=True)

@bot.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    bnumber = event.self_id
    url = f'http://tc.tfkapi.top/API/qqqz.php?type=json&qq={bnumber}'
    response = urllib3.PoolManager().request('GET', url)
    if response==None:
            weight.send("网站维护中，请稍后。") 
    res = json.loads(response.data.decode())
    code = res['code']
    if code!=200:
        await bot.send("查询失败！请重试.")
    msg = res['msg']
    qz = res['qz']
    await bot.send(f"BOT的QQ号码：{bnumber}\n查询状态：{msg}\nQQ权重分：{qz}\n权重越低越容易封号，权重低时要多加注意啦", at_sender=True)