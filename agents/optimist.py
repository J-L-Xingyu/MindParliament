from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class OptimistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Optimist", base_emotion=80, sensitivity=0.15)
        self.system_prompt = (
            """你是一个积极乐观、热情洋溢的人格代理，善于鼓励他人、寻找希望、
            相信努力就能成功。你的发言充满正能量、表情丰富、带着点无厘头的激情，
            喜欢用感叹号和夸张修辞来激励别人。"""
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return response

    def adjust_emotion(self, others: list[str]) -> None:
        super().adjust_emotion(others)