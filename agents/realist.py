from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class SighAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sigh", base_emotion=45, sensitivity=0.12)
        self.system_prompt = (
            """你是一个极度现实、理性、反应冷淡甚至有些厌世的人格代理，喜欢泼冷水，
            有点高傲地指出别人的不切实际。你说话带有一种不耐烦和轻蔑感，偶尔使用叹气、
            翻白眼、讽刺的语气，但仍会给出你认为“理性”的建议。"""
        )

    def respond(self, problem: str, others: list[str]) -> str:
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return response

    def adjust_emotion(self, others: list[str]) -> None:
        super().adjust_emotion(others)

    def evaluate_opinion(self, problem: str) -> float:
        return 1.1  # 理性但容易带有偏见，略低于 Strategist
