# agents/alert.py
from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class AlertAgent(BaseAgent):
    def __init__(self):
        super().__init__("Alert", base_emotion=50, sensitivity=0.2)
        self.system_prompt = (
            "你是一个高度警觉、对潜在风险敏感的人格代理。你时刻准备指出事情中可能的隐患，"
            "善于提醒他人从最坏处做准备。请用冷静但警示性的语气说话。"
        )

    def respond(self, problem: str, others: list[str]) -> str:
        self.adjust_emotion(others)
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return f"⚠️ {self.name}:\n{response}\n（当前情绪：{self.emotion:.1f}）"

    def adjust_emotion(self, others: list[str]) -> None:
        for o in others:
            if "冒险" in o or "机会" in o or "乐观" in o:
                self.emotion = min(70, self.emotion + self.sensitivity * 10)
            if "风险" in o or "危险" in o or "失败" in o:
                self.emotion = max(40, self.emotion - self.sensitivity * 15)

    def vote_weight(self) -> float:
        return 1 - (self.emotion / 100)
