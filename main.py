from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.realist import SighAgent
from agents.alert import NerveAgent
from agents.strategist import StrategistAgent


def run_debate(rounds: int = 2):
    print("\n🧠 欢迎来到智能人格议会！")
    problem = input("请输入你面临的决策问题：\n> ")

    agents = [
        OptimistAgent(),
        PessimistAgent(),
        SighAgent(),      # 现在是厌世风格
        NerveAgent(),
        StrategistAgent(),
    ]

    all_opinions = []

    for round_num in range(rounds):
        print(f"\n🔁 第 {round_num + 1} 轮讨论：\n")
        for agent in agents:
            agent.adjust_emotion(all_opinions)
            opinion = agent.respond(problem, all_opinions)
            all_opinions.append(f"{agent.name}: {opinion}")
            print(f"🗣️ {agent.name}（情绪值 {agent.emotion:.1f}）：\n{opinion}\n")

    print("\n📊 最终投票分析：\n")
    total_score = 0
    vote_detail = []

    for agent in agents:
        emotion_weight = agent.vote_weight()
        logic_score = agent.evaluate_opinion(problem)
        final_weight = emotion_weight * logic_score
        total_score += final_weight
        vote_detail.append((agent.name, emotion_weight, logic_score, final_weight))

        print(f"🧮 {agent.name} 投票：情绪权重={emotion_weight:.2f}，理性评分={logic_score:.2f} → 最终票权={final_weight:.2f}")

    print("\n🔚 综合建议：")
    if total_score > len(agents) * 0.5:
        print("✅ 建议尝试！综合得分 {:.2f}".format(total_score))
    else:
        print("🛑 建议保守！综合得分 {:.2f}".format(total_score))

    return all_opinions, vote_detail, total_score



if __name__ == '__main__':
    run_debate()

