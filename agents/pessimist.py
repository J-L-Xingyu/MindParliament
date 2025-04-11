# agents/pessimist.py
from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class PessimistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Pessimist", base_emotion=70, sensitivity=0.1)
        self.system_prompt = (
            "你是一个容易焦虑、倾向于看到最坏结果的悲观人格。"
            "你善于识别潜在风险、失败后果和不确定因素，请以小心翼翼、保守的语气发言。"
        )

    def respond(self, problem: str, others: list[str]) -> str:
        self.adjust_emotion(others)
        prompt = self.get_prompt(problem, others)
        response = call_gemini(prompt)
        return f"🌧️ {self.name}:\n{response}\n（当前情绪：{self.emotion:.1f}）"

    def adjust_emotion(self, others: list[str]) -> None:
        for o in others:
            if "机会" in o or "大胆" in o or "成长" in o or "勇敢" in o:
                self.emotion = max(30, self.emotion - self.sensitivity * 15)
            elif "担心" in o or "失败" in o:
                self.emotion = max(20, self.emotion - self.sensitivity * 10)
