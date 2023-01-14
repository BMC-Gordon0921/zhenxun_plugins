import random
from pathlib import Path

from nonebot import on_endswith, on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher

__zx_plugin_name__ = "答案之书"
__plugin_usage__ = """
usage：
    谁的生活不迷茫，谁的人生不迷惑。每个人都希望未卜先知，都希望掌控自己命运的罗盘，可变换莫测的世界总让我们感到失望，其实，我们的困惑并不在身外，而在我们的内心深处。我们总是希望心灵的疑惑得带一个真诚的回应，即便这个回应只是简单的“是”或“否”。

这是一本治愈系的心灵解惑书，它将带给你的不止是生活的指引，还有心灵的慰藉。

数据来源于吉林美术出版社2018年9月第1版的《神奇的答案之书》，数据著作权为原作者张权所有。

指令：

    翻看答案 + 问题  =  翻看这个问题的答案
    问题 + 翻看答案  =  翻看这个问题的答案
""".strip()
__plugin_des__ = "答案之书"
__plugin_cmd__ = [
    "翻看答案"
]
__plugin_type__ = ("群内小游戏", )
__plugin_version__ = 0.2
__plugin_author__ = "A-kirami"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}

try:
    import ujson as json
except ModuleNotFoundError:
    import json

answers_path = Path(__file__).parent / "answersbook.json"
answers = json.loads(answers_path.read_text("utf-8"))

def get_answers():
    key = random.choice(list(answers))
    return answers[key]["answer"]

answers_starts = on_startswith("翻看答案")
answers_ends = on_endswith("翻看答案")

@answers_starts.handle()
@answers_ends.handle()
async def answersbook(event: GroupMessageEvent, matcher: Matcher):
    msg = event.message.extract_plain_text().replace("翻看答案", "")
    if not msg:
        await matcher.finish("你想问什么问题呢？")
    answer = get_answers()
    await matcher.send(answer, at_sender=True)
