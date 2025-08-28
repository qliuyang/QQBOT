import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import re
from strings import CALC_REGEX, ERROR_MESSAGES
from .utils import is_allowed_group

def register_calc_command():
    """
    注册一个名为“计算”的命令处理器。
    该命令仅在白名单群组中可用，并且需要@机器人触发。
    """
    # 创建计算命令处理器，仅在指定群组中响应
    calc_cmd = on_command("计算", rule=to_me() & is_allowed_group)

    @calc_cmd.handle()
    async def calc_command(args: Message = CommandArg()):
        """
        处理“计算”命令的逻辑。
        
        参数:
            args (Message): 提取用户输入的表达式。
        """
        # 去除表达式前后空格
        expression = args.extract_plain_text().strip()
        
        # 如果表达式为空，提示用户输入内容
        if not expression:
            await calc_cmd.send(ERROR_MESSAGES["calc_no_expression"])
            return
        
        # 安全检查：仅允许合法字符组成的表达式
        if re.match(CALC_REGEX, expression):
            try:
                # 使用 eval 计算合法表达式的结果
                result = eval(expression)
                await calc_cmd.send(f"{expression} = {result}")
            except Exception as e:
                # 捕获计算过程中可能出现的异常
                await calc_cmd.send(ERROR_MESSAGES["calc_error"])
        else:
            # 表达式包含非法字符时，提示用户
            await calc_cmd.send(ERROR_MESSAGES["calc_invalid_expression"])