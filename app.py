from flask import Flask, render_template, request, jsonify
from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.alert import AlertAgent
from agents.strategist import StrategistAgent

app = Flask(__name__)

AGENTS = [
    OptimistAgent(),
    PessimistAgent(),
    AlertAgent(),
    StrategistAgent()
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    problem = data.get('problem', '')

    all_opinions = []
    messages = []
    vote_data = []
    total_score = 0

    for agent in AGENTS:
        agent.adjust_emotion(all_opinions)
        opinion = agent.respond(problem, all_opinions)
        all_opinions.append(opinion)
        messages.append({
            'name': agent.name,
            'opinion': opinion
        })

    for agent in AGENTS:
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

    suggestion = "✅ 建议尝试！" if total_score > len(AGENTS) * 0.5 else "🛑 建议保守！"

    return jsonify({
        'messages': messages,
        'votes': vote_data,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)
