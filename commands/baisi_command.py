import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group


def register_baisi_command():
    # 添加随机白丝图片功能
    baisi_cmd = on_command("随机白丝", rule=to_me() & is_allowed_group)

    @baisi_cmd.handle()
    async def baisi_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到随机白丝图片请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})")
        
        # 调用随机白丝API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URLS["baisi"])
                data = response.json()
                
                if data["code"] == 200:
                    image_url = data["data"]
                    # 发送图片
                    await baisi_cmd.send(MessageSegment.image(image_url))
                else:
                    await baisi_cmd.send(ERROR_MESSAGES["baisi_api_failed"].format(msg=data['msg']))
        except Exception as e:
            # 出现异常时发送错误消息
            nonebot.logger.error(f"获取随机白丝图片失败: {e}")
            await baisi_cmd.send(ERROR_MESSAGES["baisi_request_failed"])