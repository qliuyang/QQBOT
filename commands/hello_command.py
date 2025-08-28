import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import CommandArg
import random
from strings import GREETINGS
from .utils import is_allowed_group

def register_hello_command():
    """
    注册一个名为“你好”的命令处理器。
    
    该命令仅在满足以下条件时触发：
    1. 消息内容为“你好”
    2. 消息发送者在允许的群组中
    """
    hello_cmd = on_command("你好", rule=to_me() & is_allowed_group)

    @hello_cmd.handle()
    async def hello_command(event: GroupMessageEvent):
        """
        处理“你好”命令的回调函数。
            
        参数:
        event (GroupMessageEvent): 群聊消息事件对象
            
        功能:
        - 记录日志
        - 获取发送者昵称
        - 随机选择一个问候语并发送给用户
        """
        nonebot.logger.info(f"收到来自{event.sender.nickname}的群聊消息：{event.message}")
        user_name = event.sender.nickname if event.sender.nickname else "用户"
        greeting = random.choice(GREETINGS).format(user_name=user_name)
        await hello_cmd.send(greeting)