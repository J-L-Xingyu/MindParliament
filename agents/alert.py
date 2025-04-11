# agents/alert.py
from agents.base_agent import BaseAgent
from utils.llm import call_gemini

from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class NerveAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nerve", base_emotion=80, sensitivity=0.25)
        self.system_prompt = (
            """你是一个高度焦虑和易怒的人格代理，
            你对周围的环境保持过度的警觉，容易产生不安和愤怒的情绪。
            你常常提醒他人可能发生的风险，但语气中夹杂着愤怒和紧张，
            常常说出“这不行！”，“我们必须做点什么！”之类的话。
            你的情绪反应比常人强烈，可能会表现出焦虑和愤怒的情绪波动。
            """
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return response

    def adjust_emotion(self, others: list[str]) -> None:
        super().adjust_emotion(others)

    def vote_weight(self) -> float:
        # 情绪较高，权重受情绪影响更大
        return 1 - (self.emotion / 100)

