from nonebot import on_command, on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, GROUP, GROUP_ADMIN, GROUP_OWNER, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.log import logger
from .utils import eating_manager, Meals, config
from nonebot import require, get_bot

__zx_plugin_name__ = "吃饭小助手"
__plugin_usage__ = """
usage：
    选择恐惧症？让Bot建议你今天吃什么！吃什么：今天吃什么、中午吃啥、今晚吃啥、中午吃什么、晚上吃啥、晚上吃什么、夜宵吃啥……
    查看群菜单：菜单/群菜单/查看菜单；
    [su] 添加或移除：添加/移除 菜名；
    [su] 添加至基础菜单：加菜 菜名；
    [su] 查看基础菜单：基础菜单；
    [su] 开启/关闭按时吃饭小助手：开启/关闭小助手；
""".strip()
__plugin_des__ = "吃饭小助手"
__plugin_cmd__ = [
    "菜单/群菜单/查看菜单",
    "添加/移除",
    "加菜",
    "基础菜单",
    "开启/关闭小助手",
    "开启/关闭按时吃饭小助手",
]

greating_helper = require("nonebot_plugin_apscheduler").scheduler
eating_helper = require("nonebot_plugin_apscheduler").scheduler

__what2eat_version__ = "v0.2.6"
plugin_notes = f'''
今天吃什么？ {__what2eat_version__}
[xx吃xx]    问bot恰什么
[添加 xx]   添加菜品至群菜单
[移除 xx]   从菜单移除菜品
[加菜 xx]   添加菜品至基础菜单
[菜单]       查看群菜单
[基础菜单]查看基础菜单
[开启/关闭小助手]   开启/关闭按时吃饭小助手'''.strip()

plugin_help = on_command("吃什么帮助", permission=GROUP, priority=5, block=True)
what2eat = on_regex(r"^(今天|[早中午晚][上饭餐午]|早上|夜宵|今晚)吃(什么|啥|点啥)", permission=GROUP, priority=5, block=True)
add_group = on_command("添加", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=7, block=True)
remove_food = on_command("移除", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=5, block=True)
add_basic = on_command("加菜", permission=SUPERUSER, priority=5, block=True)
show_group = on_command("菜单", aliases={"群菜单", "查看菜单"}, permission=GROUP, priority=5, block=True)
show_basic = on_command("基础菜单", permission=SUPERUSER, priority=5, block=True)

switch_greating = on_regex(r"(开启|关闭)小助手", permission=SUPERUSER, priority=5, block=True)
add_greating = on_command("添加问候", aliases={"添加问候语"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=5, block=True)
remove_greating = on_command("删除问候", aliases={"删除问候语"}, permission=SUPERUSER, priority=5, block=True)

@plugin_help.handle()
async def _(bot: Bot):
    await plugin_help.finish(plugin_notes)

@what2eat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = eating_manager.get2eat(event)
    await what2eat.finish(msg)

@add_group.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await add_group.finish("还没输入你要添加的菜品呢~")
    elif args and len(args) == 1:
        new_food = args[0]
    else:
        await add_group.finish("添加菜品参数错误~")
    
    user_id = str(event.user_id)
    logger.info(f"User {user_id} 添加了 {new_food} 至菜单")
    msg = eating_manager.add_group_food(new_food, event)

    await add_group.finish(msg)

@add_basic.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await add_basic.finish("还没输入你要添加的菜品呢~")
    elif args and len(args) == 1:
        new_food = args[0]
    else:
        await add_basic.finish("添加菜品参数错误~")
    
    user_id = str(event.user_id)
    logger.info(f"Superuser {user_id} 添加了 {new_food} 至基础菜单")
    msg = eating_manager.add_basic_food(new_food)

    await add_basic.finish(msg)

@remove_food.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await remove_food.finish("还没输入你要移除的菜品呢~")
    elif args and len(args) == 1:
        food_to_remove = args[0]
    else:
        await remove_food.finish("移除菜品参数错误~")
    
    user_id = str(event.user_id)
    logger.info(f"User {user_id} 从菜单移除了 {food_to_remove}")
    msg = eating_manager.remove_food(food_to_remove, event)

    await remove_food.finish(msg)

@show_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = eating_manager.show_group_menu(event)
    await show_group.finish(msg)

@show_basic.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = eating_manager.show_basic_menu()
    await show_basic.finish(msg)

@switch_greating.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    args = event.get_plaintext()
    if args[:2] == "开启":
        greating_helper.resume()
        msg = f"已开启按时吃饭小助手~"
    elif args[:2] == "关闭":
        greating_helper.pause()
        msg = f"已关闭按时吃饭小助手~"

    await switch_greating.finish(msg)
    
@add_greating.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await add_basic.finish("还没输入你要添加的问候语~")
    elif args and len(args) == 1:
        await add_greating.finish("输入参数数目错误~")
    elif len(args) > 2:
        await add_greating.finish("参数太多啦~")

    msg = eating_manager.add_greating(args)
    await add_greating.finish(msg)
    
@remove_greating.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await add_basic.finish("请输入删除问候语的类别~")
    elif args and len(args) > 1:
        await add_greating.finish("参数太多啦~")

    msg = eating_manager.remove_greating(args[0])
    await remove_greating.finish(msg)

# 重置吃什么次数，包括夜宵
@eating_helper.scheduled_job("cron", hour="6,11,17,22", minute=0)
async def _():
    eating_manager.reset_eating()
    logger.info("今天吃什么次数已刷新")

# 早餐提醒
@greating_helper.scheduled_job("cron", hour=7, minute=0)
async def time_for_breakfast():
    bot = get_bot()
    msg = eating_manager.get2greating(Meals.BREAKFAST)
    if msg and len(config.groups_id) > 0:
        for group_id in config.groups_id:
            await bot.send_group_msg(group_id=int(group_id), message=msg)
        
        logger.info(f"已群发早餐提醒")

# 午餐提醒
@greating_helper.scheduled_job("cron", hour=12, minute=0)
async def time_for_lunch():
    bot = get_bot()
    msg = eating_manager.get2greating(Meals.LUNCH)
    if msg and len(config.groups_id) > 0:
        for group_id in config.groups_id:
            await bot.send_group_msg(group_id=int(group_id), message=msg)
        
        logger.info(f"已群发午餐提醒")

# 下午茶/摸鱼提醒
@greating_helper.scheduled_job("cron", hour=15, minute=0)
async def time_for_snack():
    bot = get_bot()
    msg = eating_manager.get2greating(Meals.SNACK)
    if msg and len(config.groups_id) > 0:
        for group_id in config.groups_id:
            await bot.send_group_msg(group_id=int(group_id), message=msg)
        
        logger.info(f"已群发摸鱼提醒")

# 晚餐提醒
@greating_helper.scheduled_job("cron", hour=18, minute=0)
async def time_for_dinner():
    bot = get_bot()
    msg = eating_manager.get2greating(Meals.DINNER)
    if msg and len(config.groups_id) > 0:
        for group_id in config.groups_id:
            await bot.send_group_msg(group_id=int(group_id), message=msg)
        
        logger.info(f"已群发晚餐提醒")

# 夜宵提醒
@greating_helper.scheduled_job("cron", hour=22, minute=0)
async def time_for_midnight():
    bot = get_bot()
    msg = eating_manager.get2greating(Meals.MIDNIGHT)
    if msg and len(config.groups_id) > 0:
        for group_id in config.groups_id:
            await bot.send_group_msg(group_id=int(group_id), message=msg)
        
        logger.info(f"已群发夜宵提醒")