import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group

def register_bilibili_command():
    # 添加B站用户信息查询功能
    bilibili_cmd = on_command("bilibili", rule=to_me() & is_allowed_group)

    @bilibili_cmd.handle()
    async def bilibili_command(event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
        # 获取用户ID参数
        uid = args.extract_plain_text().strip()
        
        if not uid:
            await bilibili_cmd.send(ERROR_MESSAGES["bilibili_no_uid"])
            return
            
        if not uid.isdigit():
            await bilibili_cmd.send(ERROR_MESSAGES["bilibili_invalid_uid"])
            return
        
        # 记录日志
        nonebot.logger.info(f"收到B站用户信息查询请求，用户: {event.sender.nickname}({event.sender.user_id})，查询UID: {uid}")
        
        try:
            # 调用B站用户信息API
            api_url = API_URLS["bilibili_info"].format(uid=uid)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, timeout=10.0)
                data = response.json()
                
                if data["errno"] == 0:
                    user_info = data["data"]
                    
                    # 构造用户信息文本
                    info_text = f"""🔍 B站用户信息查询结果：
                                    👤 用户昵称：{user_info['name']}
                                    🆔 用户ID：{user_info['mid']}
                                    เพศ 性别：{user_info['sex']}
                                    🎂 生日：{user_info['birthday']}
                                    📝 签名：{user_info['sign']}
                                    🏆 等级：{user_info['level']}级"""
                    
                    # 添加VIP信息
                    if user_info['vip']['status'] == 1:
                        info_text += f"\n🎖 VIP状态：{user_info['vip']['label']['text']}"
                    
                    # 添加直播间信息（如果在直播）
                    if 'live_room' in user_info and user_info['live_room']['liveStatus'] == 1:
                        info_text += f"\n🔴 正在直播：{user_info['live_room']['title']}"
                    
                    # 发送文本信息
                    await bilibili_cmd.send(info_text)
                    
                    # 如果有头像，也发送头像
                    if 'face' in user_info and user_info['face']:
                        try:
                            await bilibili_cmd.send(MessageSegment.image(file=user_info['face']))
                        except Exception as img_error:
                            nonebot.logger.warning(f"发送B站用户头像失败: {img_error}")
                else:
                    await bilibili_cmd.send(ERROR_MESSAGES["bilibili_api_error"].format(msg=data.get('errmsg', '未知错误')))
                    
        except httpx.TimeoutException:
            await bilibili_cmd.send(ERROR_MESSAGES["bilibili_request_timeout"])
        except Exception as e:
            nonebot.logger.error(f"查询B站用户信息时出错: {str(e)}")
            await bilibili_cmd.send(ERROR_MESSAGES["bilibili_query_error"].format(error=str(e)))