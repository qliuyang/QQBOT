# 字符串常量定义文件

# 帮助文本
HELP_TEXT = """我是你的QQ机器人，我可以：
1. 唱歌（@我 /唱歌）
2. 计算（@我 /计算）
3. 天气（@我 /天气 城市）
4. 笑话（@我 /笑话）
5. 问候（@我 /你好）
6. QQ头像（@我 /头像）
7. B站用户信息（@我 /bilibili UID !暂时用不起!)
8. 点歌（@我 /点歌 歌曲名）
9. AI问答（@我 /ai 问题）
10. 随机小姐姐（@我 /随机小姐姐）
11. 随机头像（@我 /随机头像）
12. 随机黑丝（@我 /随机黑丝）
13. 随机白丝（@我 /随机白丝）
14. 每日60s（@我 /60s）
直接在群聊中@我并发送以上关键词即可使用对应功能"""

# 问候语
GREETINGS = [
    "你好，{user_name}！今天过得怎么样？",
    "嗨，{user_name}！有什么我可以帮你的吗？",
    "您好，{user_name}！很高兴见到你！"
]

# 笑话列表
LOCAL_JOKES = [
    "为什么熊猫不能当厨师？因为它们只会蒸（蒸）竹！",
    "有一天，小明对妈妈说：妈妈，我想要一只小狗。妈妈说：不行，养狗太麻烦了。小明说：那我要一只小猫。妈妈说：不行，养猫也麻烦。小明说：那我要一只小鸟。妈妈说：不行，养鸟也麻烦。小明：那我要一只乌龟。妈妈：可以，乌龟好养。小明：那我要一只企鹅。妈妈：不行，企鹅是国家保护动物。小明：那我要一只恐龙。妈妈：恐龙已经灭绝了。小明：那我要一只熊猫。妈妈：熊猫是国宝。小明：那我要一只你。妈妈：我是你妈妈，不是宠物。小明：那我要一只爸爸。妈妈：爸爸是爸爸，不是宠物。小明说：那我要一只你和一只爸爸。妈妈说：我们都是人，不是宠物。小明说：那我要一只老师。妈妈说：老师是老师，不是宠物。小明说：那我要一只医生。妈妈说：医生是医生，不是宠物。小明说：那我要一只警察。妈妈说：警察是警察，不是宠物。小明说：那我要一只消防员。妈妈说：消防员是消防员，不是宠物。小明说：那我要一只解放军。妈妈说：解放军是解放军，不是宠物。小明说：那我要一只科学家。妈妈说：科学家是科学家，不是宠物。小明说：那我要一只宇航员。妈妈说：宇航员是宇航员，不是宠物。小明说：那我要一只超人。妈妈说：超人是虚构的。小明说：那我要一只机器人。妈妈说：机器人不是宠物。小明说：那我要一只AI。妈妈说：AI不是宠物。小明说：那我要一只宠物。妈妈说：好，我们去买一只宠物吧！",
    "老师：小明，你为什么上课睡觉？小明：因为梦里有你。老师：那你为什么哭？小明：因为梦醒了。",
    "医生：你怎么了？病人：医生，我觉得我是一只蛾子。医生：那你应该去看心理医生啊，为什么来找我？病人：因为你这里开着灯。",
    "小明：妈妈，我想要一只小狗。妈妈说：不行，养狗太麻烦了。小明：那我要一只小猫。妈妈：不行，养猫也麻烦。小明说：那我要一只小鸟。妈妈说：不行，养鸟也麻烦。小明：那我要一只乌龟。妈妈：可以，乌龟好养。小明：那我要一只企鹅。妈妈：不行，企鹅是国家保护动物。小明：那我要一只恐龙。妈妈：恐龙已经灭绝了。小明：那我要一只熊猫。妈妈：熊猫是国宝。小明：那我要一只你。妈妈：我是你妈妈，不是宠物。小明：那我要一只爸爸。妈妈：爸爸是爸爸，不是宠物。小明说：那我要一只你和一只爸爸。妈妈说：我们都是人，不是宠物。小明说：那我要一只老师。妈妈说：老师是老师，不是宠物。小明说：那我要一只医生。妈妈说：医生是医生，不是宠物。小明说：那我要一只警察。妈妈说：警察是警察，不是宠物。小明说：那我要一只消防员。妈妈说：消防员是消防员，不是宠物。小明说：那我要一只解放军。妈妈说：解放军是解放军，不是宠物。小明说：那我要一只科学家。妈妈说：科学家是科学家，不是宠物。小明说：那我要一只宇航员。妈妈说：宇航员是宇航员，不是宠物。小明说：那我要一只超人。妈妈说：超人是虚构的。小明说：那我要一只机器人。妈妈说：机器人不是宠物。小明说：那我要一只AI。妈妈说：AI不是宠物。小明说：那我要一只宠物。妈妈说：好，我们去买一只宠物吧！"
]

# 错误消息
ERROR_MESSAGES = {
    "calc_invalid_expression": "表达式中包含不允许的字符，只能使用数字和基本运算符",
    "calc_error": "计算出错了，请检查表达式是否正确",
    "calc_no_expression": "请输入要计算的表达式，例如：@我 计算 1+1",
    "weather_no_city": "请输入要查询的城市，例如：@我 天气 北京",
    "weather_api_failed": "获取天气信息失败：{msg}",
    "weather_request_failed": "API请求失败，使用模拟数据",
    "avatar_generating": "正在生成个性头像，请稍候...",
    "avatar_download_failed": "下载第{index}张图片失败",
    "avatar_link_failed": "获取第{index}个头像链接失败：{msg}",
    "avatar_error": "获取第{index}个头像时出错：{error}",
    "avatar_incomplete": "图片下载不完整，只下载了{count}张图片",
    "avatar_generation_error": "生成头像时出现错误: {error}",
    "bilibili_no_uid": "请输入B站用户ID，例如：@我 bilibili 315883644",
    "bilibili_invalid_uid": "用户ID必须是数字，请重新输入",
    "bilibili_request_timeout": "查询超时，请稍后再试",
    "bilibili_query_error": "查询过程中出现错误: {error}",
    "bilibili_api_error": "查询失败：{msg}",
    "music_no_keyword": "请输入要搜索的歌曲名或歌手名，例如：@我 点歌 双笙",
    "music_search_failed": "搜索失败：{msg}",
    "music_not_found": "没有找到相关歌曲，请尝试其他关键词",
    "music_url_failed": "获取播放链接失败：{msg}",
    "music_url_not_found": "未找到歌曲播放链接",
    "music_request_timeout": "查询超时，请稍后再试",
    "music_query_error": "搜索过程中出现错误: {error}",
    "meinvpic_request_failed": "获取美女图片失败，请稍后再试",
    "meinvpic_api_failed": "API请求失败：{msg}",
    "random_avatar_request_failed": "获取随机头像失败，请稍后再试",
    "random_avatar_api_failed": "API请求失败：{msg}",
    "heisi_request_failed": "获取黑丝图片失败，请稍后再试",
    "heisi_api_failed": "API请求失败：{msg}",
    "baisi_request_failed": "获取白丝图片失败，请稍后再试",
    "baisi_api_failed": "API请求失败：{msg}",
    "ai_no_question": "请输入你要询问的问题，例如：@我 ai 你好",
    "ai_all_services_unavailable": "所有AI问答服务暂时不可用，请稍后再试。"
}

# 计算表达式正则
CALC_REGEX = r'^[0-9+\-*/(). ]+$'

# API URLs
API_URLS = {
    "weather_special_tengzhou": "https://v2.xxapi.cn/api/weather?city=枣庄滕州",
    "weather_general": "https://v2.xxapi.cn/api/weather?city={city}",
    "avatar_base": "https://v2.xxapi.cn/api/profilePicture{index}?qq={qq}",
    "joke": "https://api.timelessq.com/joke",
    "bilibili_info": "https://api.timelessq.com/bilibili/info?uid={uid}",
    "music_search": "https://api.timelessq.com/music/tencent/search?keyword={keyword}",
    "music_song_url": "https://api.timelessq.com/music/tencent/songUrl?songmid={songmid}",
    "meinvpic": "https://v2.xxapi.cn/api/meinvpic",
    "random_avatar": "https://v2.xxapi.cn/api/head",
    "heisi": "https://v2.xxapi.cn/api/heisi",
    "baisi": "https://v2.xxapi.cn/api/baisi"
}

# AI API配置
AI_APIS = {
    "turing": {
        "name": "图灵API",
        "url": "https://v2.xxapi.cn/api/turing"
    }
}