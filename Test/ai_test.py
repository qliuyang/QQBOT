import asyncio
import httpx
import json

# 免费AI API配置列表
FREE_AI_APIS = [
    {
        "name": "阿里云通义千问官方API",
        "url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "model": "qwen-turbo",
        "key": "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo"  # 这里应替换为有效的API Key
    },
    {
        "name": "通义千问免费API",
        "url": "https://api.suanli.cn/v1/chat/completions",
        "model": "free:QwQ-32B",
        "key": "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo"
    }
]

async def call_ai_api(api_config, question):
    """调用单个AI API"""
    # 阿里云API和其他API的请求格式不同
    if "dashscope" in api_config["url"]:
        # 阿里云官方API格式
        payload = {
            "model": api_config["model"],
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        }
    else:
        # OpenAI兼容格式
        payload = {
            "model": api_config["model"],
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    
    headers = {
        "Authorization": f"Bearer {api_config['key']}",
        "Content-Type": "application/json"
    }
    
    print(f"正在测试 {api_config['name']}...")
    print(f"API地址: {api_config['url']}")
    print(f"使用模型: {api_config['model']}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_config["url"], 
                json=payload, 
                headers=headers, 
                timeout=30.0
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                # 根据不同API的响应格式提取回答
                if "dashscope" in api_config["url"]:
                    answer = response_data["output"]["choices"][0]["message"]["content"]
                else:
                    answer = response_data["choices"][0]["message"]["content"]
                print(f"回答: {answer}")
                return True
            else:
                print(f"错误详情: {response.text}")
                return False
                
    except httpx.TimeoutException:
        print(f"{api_config['name']} 请求超时")
        return False
    except Exception as e:
        print(f"{api_config['name']} 调用出错: {str(e)}")
        return False

async def test_all_apis():
    """测试所有AI API"""
    question = "你好，请简单介绍一下自己，回答请尽量简短"
    
    print(f"测试问题: {question}")
    print("=" * 50)
    
    success_count = 0
    for api_config in FREE_AI_APIS:
        success = await call_ai_api(api_config, question)
        if success:
            success_count += 1
        print("-" * 30)
    
    print(f"测试完成: {success_count}/{len(FREE_AI_APIS)} 个API可用")

if __name__ == "__main__":
    asyncio.run(test_all_apis())