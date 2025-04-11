# agents/strategist.py
from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class StrategistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Strategist", base_emotion=70, sensitivity=0.05)
        self.system_prompt = (
            "你是一个冷静、理性、重视长期规划与系统性思考的人格代理。"
            "你善于拆解复杂问题，分析长期风险和潜在收益，并给出可持续建议。"
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return f"🧠 {self.name}:\n{response}\n（当前情绪：{self.emotion:.1f}）"

    def adjust_emotion(self, others: list[str]) -> None:
        # 战略人格情绪变化小，暂不做调整
        pass

    def evaluate_opinion(self, problem: str) -> float:
        return 1.5  # 战略人格被赋予更高的理性评分

