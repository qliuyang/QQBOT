import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 导入并注册命令
from commands import register_commands
register_commands()

if __name__ == "__main__":
    nonebot.run()