import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from strings import API_URLS
import httpx
from .utils import is_allowed_group


def register_sixty_command():
    # 添加每日60s功能
    sixty_cmd = on_command("60s", rule=to_me() & is_allowed_group)

    @sixty_cmd.handle()
    async def sixty_command(event: GroupMessageEvent):
        nonebot.logger.info(f"收到每日60s请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})")
        
        # 调用每日60s API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://v2.xxapi.cn/api/hot60s")
                data = response.json()
                
                if data["code"] == 200:
                    image_url = data["data"]
                    # 发送图片
                    await sixty_cmd.send(MessageSegment.image(image_url))
                else:
                    await sixty_cmd.send("获取每日60s图片失败")
        except Exception as e:
            # 出现异常时发送错误消息
            nonebot.logger.error(f"获取每日60s图片失败: {e}")
            await sixty_cmd.send("获取每日60s图片失败，请稍后再试")