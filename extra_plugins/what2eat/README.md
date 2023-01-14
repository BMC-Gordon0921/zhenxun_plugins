_🍔🌮🍜🍮🍣🍻🍩 今天吃什么 🍩🍻🍣🍮🍜🌮🍔_

## 版本

v0.2.6

# nonebot-plugin-what2eat

适用于真寻 [Nonebot2](https://github.com/nonebot/nonebot2) 的 what2eat 今天吃什么插件

数据默认位于`./resource`下`data.json`与`greating.json`，可通过设置`env`下`WHAT2EAT_PATH`更改；基础菜单、群特色菜单及群友询问Bot次数会记录在该文件中：

    ```python
    WHAT2EAT_PATH="your-path-to-resource"
    ```

## 功能

1. 选择恐惧症？让Bot建议你今天吃什么！

2. 每餐每个时间段询问Bot建议上限可通过`EATING_LIMIT`修改（默认5次），每日6点、11点、17点、22点（夜宵）自动刷新：
    
    ```python
    EATING_LIMIT=99
    ```

3. 群管理可自行添加或移除群特色菜单（`data.json`下`[group_food][group_id]`）；超管可添加或移除基础菜单（`[basic_food]`）；

4. 各群特色菜单相互独立；各群每个时间段询问Bot建议次数独立；Bot会综合各群菜单+基础菜单给出建议；查看群菜单与基础菜单命令分立；

5. 提醒按时吃饭小助手：每天7、12、15、18、22点群发**问候语**提醒群友按时吃饭/摸鱼，`GROUPS_ID`设置需要群发的群号列表，形如：

    ```python
    GROUPS_ID=["123456789", "987654321"]
    ```

6. 按时吃饭小助手全局开关；

7. 吃什么帮助文案；

8. **新增** 更多的预置基础菜单，精选家常菜及八大菜系（未经核实）；

9. **新增** 初次使用该插件时，若不存在`data.json`与`greating.json`，设置`USE_PRESET_MENU`及`USE_PRESET_GREATING`可获取仓库中最新的预置菜单及问候语；若存在`data.json`与`greating.json`，则对应参数不会生效：

    ```python
    USE_PRESET_MENU=true
    USE_PRESET_GREATING=true
    ```

## 命令

1. 吃什么：今天吃什么、中午吃啥、今晚吃啥、中午吃什么、晚上吃啥、晚上吃什么、夜宵吃啥……

2. [管理或群主或超管] 添加或移除：添加/移除 菜名；

3. 查看群菜单：菜单/群菜单/查看菜单；

4. [超管] 添加至基础菜单：加菜 菜名；

5. [超管] 查看基础菜单：基础菜单；

6. [超管] 开启/关闭按时吃饭小助手：开启/关闭小助手；

## 效果

1. 案例1：

    Q：今天吃什么

    A：建议肯德基

    （……吃什么*5）

    Q：今晚吃什么

    A：你今天已经吃得够多了！

    Q：群菜单

    A：

    ---群特色菜单---

    alpha

    beta

    gamma

2. 案例2：

    [群管] Q：添加 派蒙

    A：派蒙 已加入群特色菜单~

    [超管] Q：加菜 东方馅挂炒饭

    A：东方馅挂炒饭 已加入基础菜单~

    [群管] Q：移除 东方馅挂炒饭

    A：东方馅挂炒饭 在基础菜单中，非超管不可操作哦~

## 本插件改自：

[HoshinoBot-whattoeat](https://github.com/pcrbot/whattoeat)

部分菜名参考[程序员做饭指南](https://github.com/Anduin2017/HowToCook)