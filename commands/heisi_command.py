import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group


def register_heisi_command():
    # 添加随机黑丝图片功能
    heisi_cmd = on_command("随机黑丝", rule=to_me() & is_allowed_group)

    @heisi_cmd.handle()
    async def heisi_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到随机黑丝图片请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})")
        
        # 调用随机黑丝API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URLS["heisi"])
                data = response.json()
                
                if data["code"] == 200:
                    image_url = data["data"]
                    # 发送图片
                    await heisi_cmd.send(MessageSegment.image(image_url))
                else:
                    await heisi_cmd.send(ERROR_MESSAGES["heisi_api_failed"].format(msg=data['msg']))
        except Exception as e:
            # 出现异常时发送错误消息
            nonebot.logger.error(f"获取随机黑丝图片失败: {e}")
            await heisi_cmd.send(ERROR_MESSAGES["heisi_request_failed"])