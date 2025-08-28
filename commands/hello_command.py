import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import CommandArg
import random
from strings import GREETINGS
from .utils import is_allowed_group

def register_hello_command():
    # 添加问候功能
    hello_cmd = on_command("你好", rule=to_me() & is_allowed_group)

    @hello_cmd.handle()
    async def hello_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到来自{event.sender.nickname}的群聊消息：{event.message}")
        user_name = event.sender.nickname if event.sender.nickname else "用户"
        greeting = random.choice(GREETINGS).format(user_name=user_name)
        await hello_cmd.send(greeting)