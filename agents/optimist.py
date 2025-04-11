# agents/optimist.py

from agents.base_agent import BaseAgent
from utils.llm import call_gemini

class OptimistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Optimist", base_emotion=85, sensitivity=0.1)
        self.system_prompt = (
            "你是一个充满希望与正能量的乐观人格，总是能看到问题中的机会，"
            "鼓励他人勇敢尝试、积极面对挑战。请使用鼓舞人心的语言风格。"
        )

    def respond(self, problem: str, others: list[str]) -> str:
        self.adjust_emotion(others)  # 先根据他人发言调整情绪
        prompt = self.get_prompt(problem, others)
        llm_response = call_gemini(prompt)

        return (
            f"🌞 {self.name}:\n{llm_response}\n（当前情绪：{self.emotion:.1f}）"
        )

    def adjust_emotion(self, others: list[str]) -> None:
        """
        乐观者在面对悲观言论时，会变得更兴奋；
        面对机会、希望时也会提升情绪，但幅度较小。
        """
        for opinion in others:
            if any(kw in opinion for kw in ["担心", "失败", "安稳", "风险"]):
                self.emotion = min(100, self.emotion + self.sensitivity * 20)
            elif any(kw in opinion for kw in ["机会", "成长", "挑战", "光明"]):
                self.emotion = min(100, self.emotion + self.sensitivity * 10)
            else:
                self.emotion = max(60, self.emotion - self.sensitivity * 5)
