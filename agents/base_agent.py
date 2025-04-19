from utils.llm import call_gemini

class BaseAgent:
    def __init__(self, name: str, base_emotion: float = 50.0, sensitivity: float = 0.1, tools=None):
        self.name = name
        self.base_emotion = base_emotion
        self.emotion = base_emotion
        self.sensitivity = sensitivity
        self.tools = tools or []
        self.system_prompt = ""
        self.always_search = False
        self.used_tool = False
        self.last_opinion = ""

    def respond(self, problem: str, others: list[str]) -> str:
        self.used_tool = False
        tool_insights = []

        if self.should_search(problem, others):
            for tool in self.tools:
                print(f"[🔍 TOOL] {self.name} 决定使用工具：{tool.name}")
                try:
                    result = tool.run(problem)
                    if result:
                        print(f"[📌 TOOL RESULT] {self.name} 收到搜索结果：{result[:60]}...")
                        tool_insights.append(result)
                        self.used_tool = True
                except Exception as e:
                    tool_insights.append(f"⚠️ 工具调用失败：{e}")

        reasoning = "\n".join(tool_insights)
        prompt = self.get_prompt(problem, others, reasoning)
        response = call_gemini(prompt)
        self.last_opinion = response.strip()
        return response

    def should_search(self, problem: str, others: list[str]) -> bool:
        if self.always_search:
            return True
        if self.emotion < 30 or self.emotion > 80:
            return True
        return False

    def vote_weight(self) -> float:
        return self.emotion / 100

    def adjust_emotion(self, others: list[str]) -> None:
        # 可保留当前逻辑或改为更精细的情绪模型
        pass

    def evaluate_opinion(self, problem: str) -> float:
        """可用于未来做风格化打分，目前默认 1.0"""
        return 1.0

    def get_prompt(self, problem: str, others: list[str], reasoning: str = "") -> str:
        recent_context = others[-4:] if others else []
        formatted_context = "\n".join(f"- {msg}" for msg in recent_context)

        last_opinion_section = (
            f"你上一轮说的是：\n“{self.last_opinion}”\n"
            if self.last_opinion else ""
        )

        tool_section = (
            f"你刚刚查阅了与该问题相关的资料如下，可以在接下来的发言中引用它们作为论据支撑你的立场：\n{reasoning}\n"
            if reasoning else ""
        )

        return (
            f"{self.system_prompt}\n\n"
            f"pxlfree 正在思考：\n“{problem}”\n\n"
            f"{last_opinion_section}"
            f"最近其他人格的观点：\n{formatted_context}\n\n"
            f"{tool_section}"
            f"请你首次或继续表达你的观点，你可以补充、修正或强调立场，也可以回应他人的意见（（表达赞同、反驳或补充））。"
        )
