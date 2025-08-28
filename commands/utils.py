import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

# 自定义规则：检查是否在允许的群组中
async def is_allowed_group(event) -> bool:
    # 从环境变量读取允许的群组ID列表
    ALLOWED_GROUPS_LIST = [1057980858,952765358]
    
    # 如果没有设置允许的群组，则默认允许所有
    if not ALLOWED_GROUPS_LIST:
        return True
    
    # 如果是群消息，检查群号是否在允许列表中
    if isinstance(event, GroupMessageEvent):
        return event.group_id in ALLOWED_GROUPS_LIST
    
    # 私聊消息不受限制
    return True