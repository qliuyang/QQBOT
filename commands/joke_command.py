import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from strings import LOCAL_JOKES, API_URLS, ERROR_MESSAGES
import httpx
import random
from .utils import is_allowed_group

def register_joke_command():
    # 添加笑话功能
    joke_cmd = on_command("笑话", rule=to_me() & is_allowed_group)

    @joke_cmd.handle()
    async def joke_command():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URLS["joke"])
                data = response.json()
                
                if data["errno"] == 0:
                    joke_content = data["data"]["content"]
                    await joke_cmd.send(joke_content)
                else:
                    # 如果API调用失败，使用原来的本地笑话
                    await joke_cmd.send(random.choice(LOCAL_JOKES))
        except Exception as e:
            # 出现异常时使用本地笑话库
            await joke_cmd.send(random.choice(LOCAL_JOKES))