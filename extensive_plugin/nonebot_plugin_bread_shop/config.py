#!/usr/bin/python
# -*- coding:utf-8 -*-
from enum import Enum
from nonebot import get_driver
from pydantic import BaseSettings, Extra


class Config(BaseSettings, extra=Extra.ignore):
    bread_thing: str = "面包"  # 自定义物品，改掉默认的”面包“ 此为全局
    special_thing_group = {}  # 分群设置物品 示例{"群号": "炸鸡"}

    global_bread: bool = True  # 面包默认开关
    black_bread_groups: list = []  # 黑名单
    white_bread_groups: list = []  # 白名单
    level_bread_num: int = 10  # 设置升一级所需要的面包数量（数据库不保存等级！！等级会随之而变！）

    """操作冷却（单位：秒）"""
    cd_buy: int = 3600
    cd_eat: int = 3600
    cd_rob: int = 7200
    cd_give: int = 3600
    cd_bet: int = 3600

    """操作随机值上限"""
    max_buy: int = 10
    max_eat: int = 7
    max_rob: int = 7
    max_give: int = 10
    max_bet: int = 10

    """操作随机值下限"""
    min_buy: int = 3
    min_eat: int = 3
    min_rob: int = 1
    min_give: int = 3
    min_bet: int = 5

    """设置是否操作值都由随机值决定"""
    is_random_buy: bool = True
    is_random_eat: bool = True
    is_random_rob: bool = True
    is_random_give: bool = True
    is_random_bet: bool = True

    special_buy_group: dict = {}  # 示例： {"群号": bool}
    special_eat_group: dict = {}
    special_rob_group: dict = {}
    special_give_group: dict = {}
    special_bet_group: dict = {}

    """各项强行操作的成本"""
    cost_buy: int = 800
    cost_eat: int = 200
    cost_rob: int = 400


global_config = get_driver().config
bread_config = Config(**global_config.dict())  # 载入配置


LEVEL = bread_config.level_bread_num


class CD(Enum):
    """操作冷却（单位：秒）"""
    BUY = bread_config.cd_buy
    EAT = bread_config.cd_eat
    ROB = bread_config.cd_rob
    GIVE = bread_config.cd_give
    BET = bread_config.cd_bet


class MAX(Enum):
    """操作随机值上限"""
    BUY = bread_config.max_buy
    EAT = bread_config.max_eat
    ROB = bread_config.max_rob
    GIVE = bread_config.max_give
    BET = bread_config.max_bet


class MIN(Enum):
    """操作随机值下限"""
    BUY = bread_config.min_buy
    EAT = bread_config.min_eat
    ROB = bread_config.min_rob
    GIVE = bread_config.min_give
    BET = bread_config.min_bet

class COST(Enum):
    """强行操作的成本"""
    BUY = bread_config.cost_buy
    EAT = bread_config.cost_eat
    ROB = bread_config.cost_rob


def random_config():
    """设置操作数量是否由用户指定或随机"""
    from .bread_operate import BuyEvent, EatEvent, RobEvent, GiveEvent, BetEvent
    events = [BuyEvent, EatEvent, RobEvent, GiveEvent, BetEvent]
    global_settings = [bread_config.is_random_buy, bread_config.is_random_eat, bread_config.is_random_rob,
                       bread_config.is_random_give, bread_config.is_random_bet]
    special_settings = [bread_config.special_buy_group, bread_config.special_eat_group, bread_config.special_rob_group,
                        bread_config.special_give_group, bread_config.special_bet_group]

    for event_, setting in zip(events, global_settings):
        if not setting:
            event_.set_random_global(False)

    for event_, setting in zip(events, special_settings):
        if setting:
            for group_id in setting.keys():
                event_(group_id).set_random(setting[group_id])
