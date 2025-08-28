import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

# 自定义规则：检查是否在允许的群组中
async def is_allowed_group(event) -> bool:

    ALLOWED_GROUPS_LIST = [1057980858,952765358]

    if not ALLOWED_GROUPS_LIST:
        return True
    
    if isinstance(event, GroupMessageEvent):
        return event.group_id in ALLOWED_GROUPS_LIST
    
    return True