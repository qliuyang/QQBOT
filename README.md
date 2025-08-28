# QQBot

一个基于 NoneBot2 和 OneBot V11 协议的 QQ 机器人

## 如何开始

1. 使用 `nb create` 生成项目
2. 使用 `nb plugin install` 安装插件
3. 使用 `nb run` 运行机器人

## 连接配置

本机器人使用 OneBot V11 协议连接到 QQ 客户端。

### 需要的组件

你需要一个实现了 OneBot V11 协议的 QQ 客户端，例如：
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [LLOneBot](https://github.com/LLOneBot/LLOneBot) (适用于桌面QQ)
- [OpenShamrock](https://github.com/whitechi73/OpenShamrock) (适用于安卓QQ)

### 配置说明

1. 本项目包含 [.env](file:///C:/Users/LiuYang/Desktop/py/QQBOT/.env) 配置文件，其中设置了：
   - HOST: 127.0.0.1
   - PORT: 8080
   - DEBUG: true

2. 在你的 QQ 客户端配置中，需要设置连接地址为：
   - WebSocket 反向连接地址: ws://127.0.0.1:8080/onebot/v11/ws

3. 启动顺序：
   1. 先启动本机器人 (`nb run`)
   2. 再启动 QQ 客户端

## 功能特性

- 唱歌（直接 @ 机器人）
- 计算器（calc [表达式]）
- 天气查询（weather [城市]）
- 笑话（joke）
- 问候（hello）
- 帮助（help）

## 文档

参见 [NoneBot2 官方文档](https://nonebot.dev/)