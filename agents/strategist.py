# agents/strategist.py

from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class StrategistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Strategist", base_emotion=70, sensitivity=0.05)
        self.system_prompt = (
            """你是一个冷静、理性、重视长期规划与系统性思考的人格代理。
            你擅长拆解复杂问题，分析风险与收益，语言清晰、有逻辑，
            风格略带一点疏离感但绝不情绪化，是整个系统中的“军师”角色。"""
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return response

    def adjust_emotion(self, others: list[str]) -> None:
        super().adjust_emotion(others)

    def evaluate_opinion(self, problem: str) -> float:
        return 1.5

