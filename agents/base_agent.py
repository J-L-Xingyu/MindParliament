# agents/base_agent.py

class BaseAgent:
    def __init__(self, name: str, base_emotion: float = 50.0, sensitivity: float = 0.1):
        self.name = name
        self.base_emotion = base_emotion
        self.emotion = base_emotion
        self.sensitivity = sensitivity
        self.system_prompt = ""  # 子类应设置独立人格 prompt

    def respond(self, problem: str, others: list[str]) -> str:
        raise NotImplementedError("Each Agent must implement their own respond method.")

    def adjust_emotion(self, others: list[str]) -> None:
        """
        情绪调整机制：可根据他人观点进行情绪增减。
        子类可 override 实现具体策略。
        """
        pass

    def vote_weight(self) -> float:
        """
        投票权重与情绪值挂钩，情绪值越高，权重越大。
        """
        return self.emotion / 100

    def evaluate_opinion(self, problem: str) -> float:
        """
        默认认为所有观点理性评分为 1.0。
        Strategist 等角色可重写该函数提高评分。
        """
        return 1.0

    def get_prompt(self, problem: str, others: list[str]) -> str:
        """
        构造标准 Prompt 给 LLM 使用，子类可自由调用。
        """
        recent_context = "\n".join(others[-3:]) if others else "无"
        return (
            f"{self.system_prompt}\n"
            f"当前用户的问题是：{problem}\n"
            f"其他人格的观点如下：\n{recent_context}\n"
            f"请你作为「{self.name}」角色，从你的视角给出深入、带风格的建议："
        )
