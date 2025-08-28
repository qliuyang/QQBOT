import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
import httpx
import json
import re
import asyncio
from typing import Dict, Any, Optional, List
from strings import ERROR_MESSAGES, AI_APIS
from .utils import is_allowed_group



async def call_turing_api(question: str) -> Optional[str]:
    """调用图灵API"""
    async with httpx.AsyncClient() as client:
        try:
            nonebot.logger.info("正在向图灵API发送请求")
            response = await client.get(
                AI_APIS["turing"]["url"],
                params={"msg": question},
                timeout=5.0  # 5秒超时
            )
            
            # 记录响应状态码和耗时
            nonebot.logger.info(f"收到图灵API响应，状态码: {response.status_code}, 耗时: {response.elapsed.total_seconds():.2f}s")
            
            # 处理HTTP错误
            if response.status_code >= 400:
                nonebot.logger.error(f"图灵API请求错误，状态码: {response.status_code}")
                return None
            
            # 解析响应
            data = response.json()
            if data["code"] == 200:
                return data["data"]
            else:
                nonebot.logger.error(f"图灵API返回错误: {data['msg']}")
                return None
                
        except httpx.TimeoutException:
            nonebot.logger.warning("图灵API请求超时")
            return None
            
        except httpx.NetworkError as e:
            nonebot.logger.error(f"图灵API网络错误: {str(e)}")
            return None
            
        except Exception as e:
            nonebot.logger.error(f"调用图灵API时发生未知错误: {str(e)}", exc_info=True)
            return None

def register_ai_command():
    """注册AI问答命令处理器"""
    ai_cmd = on_command("ai", rule=to_me() & is_allowed_group)
    help_cmd = on_command("ai帮助", rule=to_me() & is_allowed_group)

    @ai_cmd.handle()
    async def handle_ai_command(event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
        """处理AI问答命令"""
        # 获取用户问题
        question = args.extract_plain_text().strip()
        
        if not question:
            await ai_cmd.send(ERROR_MESSAGES["ai_no_question"])
            return
        
        # 记录日志
        nonebot.logger.info(f"收到AI问答请求，用户: {event.sender.nickname}({event.sender.user_id})，问题: {question}")
        
        # 直接使用图灵API
        try:
            turing_response = await call_turing_api(question)
            
            if turing_response:
                # 清理AI回答内容
                # 构建回复消息
                reply = MessageSegment.text(turing_response)
                
                await ai_cmd.send(reply)
                return
            else:
                nonebot.logger.error("图灵API返回数据格式错误")
                
        except Exception as e:
            error_msg = f"调用图灵API时发生错误: {str(e)}"
            nonebot.logger.error(error_msg)
        
        # 如果所有API都失败了
        await ai_cmd.send(ERROR_MESSAGES["ai_all_services_unavailable"])