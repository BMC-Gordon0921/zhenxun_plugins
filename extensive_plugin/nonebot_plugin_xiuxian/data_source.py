from pathlib import Path
import json

DATABASE = Path() / "data" / "xiuxian"


class JsonDate:
    """处理JSON数据"""

    def __init__(self):
        """json文件路径"""
        self.root_jsonpath = DATABASE / "灵根.json"
        self.level_rate_jsonpath = DATABASE / "突破概率.json"
        self.Reward_that_jsonpath = DATABASE / "悬赏令.json"
        self.level_jsonpath = DATABASE / "境界.json"
        self.sect_json_pth = DATABASE / "宗门玩法配置.json"
        self.shop_jsonpath = DATABASE / "goods.json"
        self.BACKGROUND_FILE = DATABASE / "image" / "background.png"
        self.BANNER_FILE = DATABASE / "image" / "banner.png"
        self.FONT_FILE = DATABASE / "font" / "sarasa-mono-sc-regular.ttf"

    def level_data(self):
        """境界数据"""
        with open(self.level_jsonpath, 'r', encoding='utf-8') as e:
            a = e.read()
            data = json.loads(a)
            return data

    def sect_config_data(self):
        """宗门玩法配置"""
        with open(self.sect_json_pth, "r", encoding="utf-8") as fp:
            file = fp.read()
            config_data = json.loads(file)
            return config_data

    def root_data(self):
        """获取灵根数据"""
        with open(self.root_jsonpath, 'r', encoding='utf-8') as e:
            file_data = e.read()
            data = json.loads(file_data)
            return data

    def level_rate_data(self):
        """获取境界突破概率"""
        with open(self.level_rate_jsonpath, 'r', encoding='utf-8') as e:
            file_data = e.read()
            data = json.loads(file_data)
            return data

    def reward_that_data(self):
        """获取悬赏令信息"""
        with open(self.Reward_that_jsonpath, 'r', encoding='utf-8') as e:
            file_data = e.read()
            data = json.loads(file_data)
            return data

    def shop_data(self):
        """获取物品信息"""
        with open(self.shop_jsonpath, 'r', encoding='utf-8') as e:
            file_data = e.read()
            data = json.loads(file_data)
            return data

    def my_test_file(self, pathfile):
        with open(pathfile, 'r', encoding='utf-8') as e:
            file_data = e.read()
            data = json.loads(file_data)
            return data


jsondata = JsonDate()


if __name__ == '__main__':
    P =r"C:\Users\cyberway\Desktop\xiuxian\nonebot_plugin_xiuxian\nonebot_plugin_xiuxian\nonebot_plugin_xiuxian\xiuxian\goods.json"
    a = JsonDate().my_test_file(pathfile=P)
    for i in a.values():
        print(i)
    # pprint(a["结丹境圆满"]["power"])
    # from datetime import datetime
    # print(datetime.now())
    # if isinstance("2022-09-08 00:42:50.279352", datetime):
    #     print('11')