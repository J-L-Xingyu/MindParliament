from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.realist import RealistAgent
from agents.alert import AlertAgent
from agents.strategist import StrategistAgent


def run_debate():
    print("\n🧠 欢迎来到智能人格议会！")
    problem = input("请输入你面临的决策问题：\n> ")

    agents = [
        OptimistAgent(),
        PessimistAgent(),
        # RealistAgent(),
        AlertAgent(),
        StrategistAgent(),
    ]

    rounds = 1
    all_opinions = []

    for round_num in range(rounds):
        print(f"\n🔁 第 {round_num + 1} 轮讨论：\n")
        for agent in agents:
            agent.adjust_emotion(all_opinions)
            opinion = agent.respond(problem, all_opinions)
            all_opinions.append(opinion)
            print(f"{agent.name}：\n{opinion}\n")

    print("\n📊 最终投票：")
    total_score = 0
    for agent in agents:
        emotion_weight = agent.vote_weight()
        logic_weight = agent.evaluate_opinion(problem)
        final_weight = emotion_weight * logic_weight
        total_score += final_weight

        print(f"{agent.name}：情绪={emotion_weight:.2f} 理性={logic_weight:.2f} → 权重={final_weight:.2f}")

    print("\n🔚 综合建议：")
    if total_score > len(agents) * 0.5:
        print("✅ 建议尝试！")
    else:
        print("🛑 建议保守！")


if __name__ == '__main__':
    run_debate()

