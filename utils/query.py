from utils.llm import call_gemini

def generate_search_query(problem: str, role: str) -> str:
    prompt = f"""
你是一个人格代理，角色是「{role}」。
你需要围绕下面的问题，生成一条用于搜索引擎（如 Google）的有效关键词组合：

问题：「{problem}」

要求：
- 不要解释理由，直接输出关键词
- 尽量具体（如“暴雨天 出门 风险”）
- 不要长句，最多8个词以内
"""
    query = call_gemini(prompt).strip()
    print(f"[🧠 搜索生成器] 为 {role} 生成关键词：{query}")
    return query
