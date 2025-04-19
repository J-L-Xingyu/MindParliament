import os
import requests
from utils.query import generate_search_query

class SearchTool:
    query_cache = {}  # ⬅️ 所有角色共享的全局缓存：{(problem, role): result}

    def __init__(self, role_name: str):
        self.name = "SearchTool"
        self.role_name = role_name
        self.api_key = os.getenv("SERPAPI_API_KEY")

    def run(self, problem: str) -> str:
        cache_key = (problem.strip(), self.role_name)

        # ✅ 查询缓存
        if cache_key in SearchTool.query_cache:
            print(f"[⚡ CACHE] 使用缓存查询结果：{cache_key}")
            return SearchTool.query_cache[cache_key]

        # ❌ 缓存未命中，开始真正请求
        if not self.api_key:
            return "⚠️ SERPAPI_API_KEY 未设置"

        query = generate_search_query(problem, self.role_name)

        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": 5
        }

        print(f"[🔍 SearchTool] 正在搜索：{query}")

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            results = []
            if 'organic_results' in data:
                for result in data['organic_results']:
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    if snippet:
                        results.append(f"🔍 「{title}」：{snippet}")
                    if len(results) >= 3:
                        break

            if results:
                final_result = "\n".join(results)
                print(f"[📚 SearchTool] 缓存新查询：{cache_key}")
                SearchTool.query_cache[cache_key] = final_result
                return final_result

        except Exception as e:
            error_msg = f"⚠️ 搜索失败：{str(e)}"
            SearchTool.query_cache[cache_key] = error_msg
            return error_msg

        fallback_msg = "（我尝试查找了一些资料，但没有找到明确的信息。）"
        SearchTool.query_cache[cache_key] = fallback_msg
        return fallback_msg
