import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group


def register_meinvpic_command():
    # 添加随机小姐姐图片功能
    meinvpic_cmd = on_command("随机小姐姐", rule=to_me() & is_allowed_group)

    @meinvpic_cmd.handle()
    async def meinvpic_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到随机小姐姐图片请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})")
        
        # 调用随机小姐姐API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URLS["meinvpic"])
                data = response.json()
                
                if data["code"] == 200:
                    image_url = data["data"]
                    # 发送图片
                    await meinvpic_cmd.send(MessageSegment.image(image_url))
                else:
                    await meinvpic_cmd.send(ERROR_MESSAGES["meinvpic_api_failed"].format(msg=data['msg']))
        except Exception as e:
            # 出现异常时发送错误消息
            nonebot.logger.error(f"获取随机小姐姐图片失败: {e}")
            await meinvpic_cmd.send(ERROR_MESSAGES["meinvpic_request_failed"])