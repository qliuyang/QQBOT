import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, PrivateMessageEvent
from .utils import is_allowed_group

def register_sing_command():
    """
    注册唱歌命令处理器
    该命令需要@机器人且在允许的群组中触发
    """
    # 创建唱歌命令处理器，使用组合规则：@机器人 + 指定群组
    sing = on_command("唱歌", rule=to_me() & is_allowed_group)
    
    @sing.handle()
    async def _(event: GroupMessageEvent | PrivateMessageEvent):
        """
        命令处理逻辑
        当用户发送"唱歌"指令时，机器人将发送一段音频和一个表情
        """
        # 发送本地存储的introduce.mp3音频文件
        await sing.send(MessageSegment.record(file=r"C:\Users\LiuYang\Desktop\py\QQBOT\Audio\introduce.mp3"))
        
        # 发送ID为1的表情（通常是[微笑]表情）
        await sing.send(MessageSegment.face(id_=1))