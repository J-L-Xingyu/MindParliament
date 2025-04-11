import os
from google import genai

# 设置 API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAsskINt8Eap0bACMTAgjv24K5XKF7ZUJg"

# 如果你需要使用本地代理（如科学上网工具），取消注释下面两行
os.environ["http_proxy"] = "http://127.0.0.1:10887"
os.environ["https_proxy"] = "http://127.0.0.1:10887"

# 创建客户端并配置 API Key
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# 定义调用生成内容的函数
def call_gemini(prompt: str, model_name="gemini-2.0-flash"):
    # 调用模型生成内容
    response = client.models.generate_content(
        model=model_name,
        contents=prompt + "   简单表明你的观点"
    )
    return response.text.strip()  # 返回生成的文本

# 测试调用
# response_text = call_gemini("Explain how AI works in a few words")
# print(response_text)
