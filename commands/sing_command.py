import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, PrivateMessageEvent
from .utils import is_allowed_group

def register_sing_command():
    # 修改唱歌命令的定义
    sing = on_command("唱歌", rule=to_me() & is_allowed_group)
    
    @sing.handle()
    async def _(event: GroupMessageEvent | PrivateMessageEvent):
        await sing.send(MessageSegment.record(file=r"C:\Users\LiuYang\Desktop\py\QQBOT\Audio\introduce.mp3"))
        await sing.send(MessageSegment.face(id_=1))