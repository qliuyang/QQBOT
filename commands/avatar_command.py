import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from strings import ERROR_MESSAGES, API_URLS
import httpx
import os
from io import BytesIO
from PIL import Image
from .utils import is_allowed_group

def register_avatar_command():
    """
    注册QQ头像生成功能的命令处理器。
    命令触发词："头像"
    触发条件：@机器人且在允许的群组中
    """
    avatar_cmd = on_command("头像", rule=to_me() & is_allowed_group)

    @avatar_cmd.handle()
    async def avatar_command(event: GroupMessageEvent):
        """
        处理QQ头像生成请求。
        
        参数:
            event (GroupMessageEvent): 群消息事件对象
        """
        # 获取用户QQ号
        qq_number = event.sender.user_id
        
        # 记录日志
        nonebot.logger.info(f"收到QQ头像生成请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})，目标QQ: {qq_number}")
        
        try:
            # 发送头像生成中提示消息
            await avatar_cmd.send(ERROR_MESSAGES["avatar_generating"])
            
            # 构建四个API地址
            api_urls = [
                API_URLS["avatar_base"].format(index=1, qq=qq_number),
                API_URLS["avatar_base"].format(index=2, qq=qq_number),
                API_URLS["avatar_base"].format(index=3, qq=qq_number),
                API_URLS["avatar_base"].format(index=4, qq=qq_number)
            ]
            
            # 存储下载的图片
            images = []
            
            # 异步下载所有图片
            async with httpx.AsyncClient() as client:
                for i, url in enumerate(api_urls):
                    try:
                        # 获取图片链接
                        response = await client.get(url, timeout=10.0)
                        data = response.json()
                        
                        if data["code"] == 200:
                            image_url = data["data"]
                            # 下载图片
                            image_response = await client.get(image_url)
                            if image_response.status_code == 200:
                                images.append(Image.open(BytesIO(image_response.content)))
                            else:
                                # 下载失败提示
                                await avatar_cmd.send(ERROR_MESSAGES["avatar_download_failed"].format(index=i+1))
                                return
                        else:
                            # API调用失败提示
                            await avatar_cmd.send(ERROR_MESSAGES["avatar_link_failed"].format(index=i+1, msg=data['msg']))
                            return
                    except Exception as e:
                        # 出错提示
                        await avatar_cmd.send(ERROR_MESSAGES["avatar_error"].format(index=i+1, error=str(e)))
                        return
            
            # 检查是否成功下载了4张图片
            if len(images) != 4:
                await avatar_cmd.send(ERROR_MESSAGES["avatar_incomplete"].format(count=len(images)))
                return
            
            # 创建一个大图来组合四张小图 (2x2布局)
            target_size = (400, 400)  # 每张图片调整为400x400
            combined_image = Image.new('RGB', (800, 800), (255, 255, 255))  # 创建800x800的白色背景图
            
            # 调整图片大小并粘贴到组合图上
            for i, img in enumerate(images):
                # 调整图片大小
                img_resized = img.resize(target_size)
                
                # 计算位置 (2x2网格)
                x = (i % 2) * 400
                y = (i // 2) * 400
                
                # 粘贴图片
                combined_image.paste(img_resized, (x, y))
            
            # 保存组合图片到临时文件
            temp_path = f"temp_avatar_{qq_number}.jpg"
            combined_image.save(temp_path, "JPEG")
            
            # 发送组合后的图片
            await avatar_cmd.send(MessageSegment.image(file=f"file:///{os.path.abspath(temp_path)}"))
            
            # 清理临时文件
            os.remove(temp_path)
            
        except Exception as e:
            # 记录错误日志
            nonebot.logger.error(f"生成QQ头像时出错: {str(e)}")
            # 发送错误提示
            await avatar_cmd.send(ERROR_MESSAGES["avatar_generation_error"].format(error=str(e)))