import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from strings import ERROR_MESSAGES, API_URLS
import httpx
from .utils import is_allowed_group

def register_music_command():
    """注册音乐点播命令处理器"""
    # 创建点歌命令处理器，仅响应@机器人且在允许的群组中
    music_cmd = on_command("点歌", rule=to_me() & is_allowed_group)

    @music_cmd.handle()
    async def music_command(event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
        # 提取搜索关键词
        keyword = args.extract_plain_text().strip()
        
        if not keyword:
            # 关键词为空时发送提示信息
            await music_cmd.send(ERROR_MESSAGES["music_no_keyword"])
            return
        
        # 记录点歌请求日志
        nonebot.logger.info(f"收到音乐搜索请求，用户: {event.sender.nickname}({event.sender.user_id})，搜索关键词: {keyword}")
        
        try:
            # 构建搜索URL并调用音乐搜索API
            search_url = API_URLS["music_search"].format(keyword=keyword)
            
            async with httpx.AsyncClient() as client:
                # 搜索歌曲
                search_response = await client.get(search_url, timeout=10.0)
                search_data = search_response.json()
                
                # 检查API返回状态
                if search_data["errno"] != 0:
                    # 搜索失败时发送错误信息
                    await music_cmd.send(ERROR_MESSAGES["music_search_failed"].format(msg=search_data.get('errmsg', '未知错误')))
                    return
                
                # 检查是否有搜索结果
                if not search_data["data"]["list"]:
                    # 没有找到歌曲时发送提示
                    await music_cmd.send(ERROR_MESSAGES["music_not_found"])
                    return
                
                # 提取歌曲列表
                song_list = search_data["data"]["list"]
                info_texts = []
                
                # 构建前5首歌曲的信息文本（最多显示5首）
                for i, song in enumerate(song_list[:5]):
                    # 提取歌曲基本信息
                    songmid = song["songmid"]
                    songname = song["songname"]
                    singer_names = "、".join([singer["name"] for singer in song["singer"]])
                    albumname = song["albumname"]
                    
                    # 格式化歌曲信息
                    info_text = f"""🎵 第{i+1}首：
歌曲：{songname}
歌手：{singer_names}
专辑：{albumname}"""
                    info_texts.append(info_text)
                
                # 发送整理后的歌曲列表信息
                await music_cmd.send("\n\n".join(info_texts))
                
                # 尝试播放第一首可播放的歌曲
                for song in song_list:
                    try:
                        # 获取当前歌曲ID
                        songmid = song["songmid"]
                        
                        # 调用API获取播放链接
                        song_url_api = API_URLS["music_song_url"].format(songmid=songmid)
                        song_response = await client.get(song_url_api, timeout=10.0)
                        song_data = song_response.json()
                        
                        # 检查API返回结果
                        if song_data["errno"] == 0 and song_data["data"]:
                            # 提取播放地址
                            play_url = song_data["data"][0]["url"]
                            
                            if play_url:
                                # 发送语音消息播放歌曲
                                await music_cmd.send(MessageSegment.record(file=play_url))
                                return  # 成功播放后退出循环
                    except Exception as e:
                        # 如果当前歌曲播放失败，尝试下一首
                        continue
                
                # 如果所有歌曲都播放失败
                await music_cmd.send("无法播放任何歌曲")
                
        except httpx.TimeoutException:
            # 处理请求超时情况
            await music_cmd.send(ERROR_MESSAGES["music_request_timeout"])
        except Exception as e:
            # 记录并处理其他异常
            nonebot.logger.error(f"搜索音乐时出错: {str(e)}")
            await music_cmd.send(ERROR_MESSAGES["music_query_error"].format(error=str(e)))