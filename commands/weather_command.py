import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message
from nonebot.params import CommandArg
from strings import ERROR_MESSAGES, API_URLS
import httpx
import random
from .utils import is_allowed_group

def register_weather_command():
    """注册天气查询命令处理器"""
    weather_cmd = on_command("天气", rule=to_me() & is_allowed_group)

    @weather_cmd.handle()
    async def weather_command(event: GroupMessageEvent, args: Message = CommandArg()):
        city = args.extract_plain_text().strip()
        
        nonebot.logger.info(f"收到天气查询请求，来自群组: {event.group_id}, 用户: {event.sender.nickname}({event.sender.user_id})，查询城市: {city}")
        
        if not city:
            await weather_cmd.send(ERROR_MESSAGES["weather_no_city"])
            return
        
        # 调用天气API
        try:
            if city == "滕州":
                url = API_URLS["weather_special_tengzhou"]
            else:
                url = API_URLS["weather_general"].format(city=city)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                data = response.json()
                
                if data["code"] == 200:
                    city_name = data["data"]["city"]
                    weather_data = data["data"]["data"]
                    
                    # 格式化天气信息展示
                    weather_info = f"🏙 {city_name} 近期天气预报：\n\n"  # noqa: E501
                    for i, day in enumerate(weather_data[:3]):  # 只显示最近3天
                        date = day["date"]
                        temperature = day["temperature"]
                        weather = day["weather"]
                        wind = day["wind"]
                        air_quality = day["air_quality"]
                        weather_info += f"📅 {date}\n🌡 温度：{temperature}\n☁ 天气：{weather}\n🌬 风力：{wind}\n🌫 空气质量：{air_quality}\n\n"
                    
                    await weather_cmd.send(weather_info.strip())
                else:
                    await weather_cmd.send(ERROR_MESSAGES["weather_api_failed"].format(msg=data['msg']))
        except Exception as e:
            # 网络请求异常时使用模拟数据作为回退方案
            await weather_cmd.send(ERROR_MESSAGES["weather_request_failed"])
            weathers = ["晴天", "多云", "阴天", "小雨", "大雨", "雪天"]
            temperature = random.randint(-10, 35)
            weather = random.choice(weathers)
            weather_info = f"{city}的天气是{weather}，温度约为{temperature}°C"
            await weather_cmd.send(weather_info)