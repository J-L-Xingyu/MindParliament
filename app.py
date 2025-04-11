from flask import Flask, render_template, request, jsonify
from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.alert import NerveAgent
from agents.strategist import StrategistAgent
from agents.realist import SighAgent
from utils.llm import call_gemini

app = Flask(__name__)

AGENTS = [
    OptimistAgent(),
    PessimistAgent(),
    NerveAgent(),
    SighAgent(),
    StrategistAgent()
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    problem = data.get('problem', '')
    rounds = 2  # 你可以自由设定为 2 或 3 轮对话

    agents = [
        OptimistAgent(),
        PessimistAgent(),
        SighAgent(),
        NerveAgent(),
        StrategistAgent()
    ]

    all_opinions = []
    messages = []
    vote_data = []
    total_score = 0

    for round_num in range(rounds):
        for agent in agents:
            agent.adjust_emotion(all_opinions)
            opinion = agent.respond(problem, all_opinions)
            all_opinions.append(f"{agent.name}: {opinion}")
            messages.append({
                'name': agent.name,
                'opinion': opinion
            })

    for agent in agents:
        e = agent.vote_weight()
        l = agent.evaluate_opinion(problem)
        w = e * l
        total_score += w
        vote_data.append({
            'name': agent.name,
            'emotion': round(e, 2),
            'logic': round(l, 2),
            'weight': round(w, 2)
        })

    suggestion = generate_llm_summary(problem, messages, vote_data)


    return jsonify({
        'messages': messages,
        'votes': vote_data,
        'suggestion': suggestion
    })

def generate_llm_summary(problem: str, messages: list[dict], votes: list[dict]) -> str:
    def format_opinions():
        lines = []
        for msg in messages:
            lines.append(f"- {msg['name']}: {msg['opinion']}")
        return "\n".join(lines)

    def format_votes():
        lines = []
        for v in votes:
            lines.append(f"- {v['name']}: 情绪 {v['emotion']:.2f}, 理性 {v['logic']:.2f}, 得分 {v['weight']:.2f}")
        return "\n".join(lines)

    prompt = f"""
你是一个会议总结者，请根据以下人格发言和投票结果，给出一个温柔理性、有逻辑的总结性建议。

🧠 用户的问题是：
「{problem}」

🗣️ 脑内人格多轮发言如下：
{format_opinions()}

📊 人格的投票如下（得分 = 情绪 * 理性）：
{format_votes()}

请你生成一个简洁清晰的最终总结，包括：
1. 最终建议（如：建议尝试 or 建议保守）
2. 简要理由（哪些人格支持、是否分歧、整体情绪如何）
3. 总体语气保持理性、温和，像是会议主持人的风格。
"""

    response = call_gemini(prompt)
    return response.strip()


if __name__ == '__main__':
    app.run(debug=True)
