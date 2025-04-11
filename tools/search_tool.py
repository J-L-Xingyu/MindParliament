class SearchTool:
    def __init__(self, bias_keywords: list[str]):
        self.name = "SearchTool"
        self.bias_keywords = bias_keywords

    def run(self, problem: str) -> str:
        # 构造“拟搜索”语句（未来可接 API）
        search_query = f"{problem} + {' + '.join(self.bias_keywords)}"
        result = f"搜索发现：关于“{problem}”，有案例强调 {self.bias_keywords[0]} 的重要性。"
        return result
