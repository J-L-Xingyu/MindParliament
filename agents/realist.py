from agents.base_agent import BaseAgent

class RealistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Realist", base_emotion=70, sensitivity=0.05)

    def respond(self, problem: str, others: list[str]) -> str:
        # Realist 不容易激动，但稍微会受观点影响
        support_count = sum("机会" in o or "成长" in o for o in others)
        worry_count = sum("担心" in o or "风险" in o for o in others)

        if support_count > worry_count:
            self.emotion += 3
        elif worry_count > support_count:
            self.emotion -= 3

        # clamp
        self.emotion = max(40, min(80, self.emotion))

        return (
            f"⚖️ {self.name}:\n"
            f"我理解你正在面对『{problem}』。\n"
            f"在我看来，做决定前需要了解更多实际信息，比如收入变化、生活成本、环境差异等。\n"
            f"目前倾向于先调研，再做出理性判断。（当前情绪：{self.emotion}）"
        )

    def vote_weight(self) -> float:
        # 越接近 60，越偏中间
        return 0.5 + (self.emotion - 60) / 100  # 大约在 0.4~0.7 之间

    def adjust_emotion(self, others: list[str]) -> None:
        # 可以有实际逻辑
        pass


