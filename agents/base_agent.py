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
        if not others:
            return

        recent = others[-4:]  # 只看最近4条观点
        delta = 0
        lower_name = self.name.lower()

        for opinion in recent:
            text = opinion.lower()
            if lower_name in text and any(word in text for word in ["赞同", "支持", "认同", "同意", "说得对"]):
                delta += 10
            elif lower_name in text and any(word in text for word in ["太激进", "我反对", "不现实", "我不同意", "太保守"]):
                delta -= 12
            elif any(word in text for word in ["冲", "谨慎", "小心", "放手", "失败", "自由"]):
                if self.name in ["Optimist"] and any(x in text for x in ["自由", "冲", "放手"]):
                    delta += 5
                elif self.name in ["Pessimist", "Alert"] and any(x in text for x in ["谨慎", "失败", "小心"]):
                    delta += 5
                else:
                    delta -= 3

        self.emotion = max(0, min(100, self.emotion + delta))

    def vote_weight(self) -> float:
        return self.emotion / 100

    def evaluate_opinion(self, problem: str) -> float:
        return 1.0

    def find_reply_target(self, others: list[str]) -> str:
        """
        简单回应机制：从其他人格观点中选一个进行引用或评论。
        """
        if not others:
            return ""
        for message in reversed(others):
            if self.name not in message:
                return message.strip()
        return others[-1]  # fallback

    def get_prompt(self, problem: str, others: list[str]) -> str:
        recent_context = "\n".join(others[-3:]) if others else "无"
        reply_target = self.find_reply_target(others)
        reply_part = f"你可以选择引用并评论以下观点：\n“{reply_target}”\n" if reply_target else ""
        return (
            f"{self.system_prompt}\n"
            f"当前用户的问题是：{problem}\n"
            f"其他人格的观点如下：\n{recent_context}\n"
            f"{reply_part}请你作为「{self.name}」角色，从你的视角给出语气贴合你的性格的回应，避免展开论述："
        )
