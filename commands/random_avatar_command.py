import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group


def register_random_avatar_command():
    # 添加随机头像功能
    random_avatar_cmd = on_command("随机头像", rule=to_me() & is_allowed_group)

    @random_avatar_cmd.handle()
    async def random_avatar_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到随机头像请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})")
        
        # 调用随机头像API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URLS["random_avatar"])
                data = response.json()
                
                if data["code"] == 200:
                    image_url = data["data"]
                    # 发送图片
                    await random_avatar_cmd.send(MessageSegment.image(image_url))
                else:
                    await random_avatar_cmd.send(ERROR_MESSAGES["random_avatar_api_failed"].format(msg=data['msg']))
        except Exception as e:
            # 出现异常时发送错误消息
            nonebot.logger.error(f"获取随机头像失败: {e}")
            await random_avatar_cmd.send(ERROR_MESSAGES["random_avatar_request_failed"])