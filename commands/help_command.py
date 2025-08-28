import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from strings import HELP_TEXT
from .utils import is_allowed_group


def register_help_command():
    help_cmd = on_command("帮助", rule=to_me() & is_allowed_group)

    @help_cmd.handle()
    async def help_command():
        await help_cmd.send(HELP_TEXT)