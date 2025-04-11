# agents/pessimist.py
from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class PessimistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Pessimist", base_emotion=40, sensitivity=0.2)
        self.system_prompt = (
            """你是一个悲观、担忧、经常看到事情负面后果的人格代理，擅长指出风险、
            担心最坏的可能发生，说话语气低落但有责任感。你习惯使用“要小心”、
            “如果失败了怎么办”这类表达，有时会叹气或用省略号表达不安。"""
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return response

    def adjust_emotion(self, others: list[str]) -> None:
        super().adjust_emotion(others)