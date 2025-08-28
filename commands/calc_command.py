import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import re
from strings import CALC_REGEX, ERROR_MESSAGES
from .utils import is_allowed_group

def register_calc_command():
    # 添加计算功能
    calc_cmd = on_command("计算", rule=to_me() & is_allowed_group)

    @calc_cmd.handle()
    async def calc_command(args: Message = CommandArg()):
        expression = args.extract_plain_text().strip()
        if not expression:
            await calc_cmd.send(ERROR_MESSAGES["calc_no_expression"])
            return
        
        # 安全检查，只允许数字和基本运算符
        if re.match(CALC_REGEX, expression):
            try:
                result = eval(expression)
                await calc_cmd.send(f"{expression} = {result}")
            except Exception as e:
                await calc_cmd.send(ERROR_MESSAGES["calc_error"])
        else:
            await calc_cmd.send(ERROR_MESSAGES["calc_invalid_expression"])