import gradio as gr
import time
from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.alert import AlertAgent
from agents.strategist import StrategistAgent

AGENTS = [
    OptimistAgent(), PessimistAgent(), AlertAgent(), StrategistAgent()
]

AVATARS = {
    "Optimist": "optimist.png",
    "Pessimist": "optimist.png",
    "Alert": "optimist.png",
    "Strategist": "optimist.png"
}

COLORS = {
    "Optimist": "#fff6c5",
    "Pessimist": "#dbe5f4",
    "Alert": "#e6dcf0",
    "Strategist": "#f8d3d3"
}

TEXT_COLORS = {
    "Optimist": "#2d2a00",
    "Pessimist": "#1e3a5f",
    "Alert": "#4a3860",
    "Strategist": "#5a1c1c"
}

def render_agent_message(agent, content, align_right=False):
    bg = COLORS[agent.name]
    fg = TEXT_COLORS[agent.name]
    avatar = AVATARS[agent.name]
    side_class = "right" if align_right else "left"
    return f"""
    <div class='message {side_class}'>
        <div class='avatar'>
            <img src="{avatar}" width="48" height="48" style="border-radius: 50%; border: 2px solid #ccc;"/>
        </div>
        <div class='bubble' style='background:{bg};color:{fg};'>{content}</div>
    </div>
    """

def run_debate(problem):
    all_opinions = []
    chat_html = "<div class='chat-box'>"

    for idx, agent in enumerate(AGENTS):
        side = idx % 2 == 1  # alternate sides
        yield chat_html + f"<div class='message {'right' if side else 'left'} thinking'><div class='avatar'><img src='/static/{AVATARS[agent.name]}'/></div><div class='bubble'>......</div></div></div>"
        time.sleep(0.8)
        agent.adjust_emotion(all_opinions)
        opinion = agent.respond(problem, all_opinions)
        all_opinions.append(opinion)
        chat_html += render_agent_message(agent, opinion, align_right=side)
        yield chat_html + "</div>"
        time.sleep(0.5)

    total_score = 0
    vote_detail = ""
    for agent in AGENTS:
        e = agent.vote_weight()
        l = agent.evaluate_opinion(problem)
        w = e * l
        total_score += w
        vote_detail += f"<li>{agent.name}：情绪={e:.2f} 理性={l:.2f} → 权重={w:.2f}</li>"

    suggestion = "✅ 建议尝试！" if total_score > len(AGENTS) * 0.5 else "🛑 建议保守！"

    chat_html += f"""
    <div class='vote-box'>
      <div class='vote-header'>📊 最终投票：</div>
      <ul>{vote_detail}</ul>
      <div class='final'>🔚 综合建议：<strong>{suggestion}</strong></div>
    </div></div>
    """
    yield chat_html

with gr.Blocks(css="""
body {
  font-family: 'Fredoka', sans-serif;
  background: #fffaf3;
  padding: 2rem;
}

h1 {
  text-align: center;
  color: #2e1f0f;
  font-size: 28px;
  margin-bottom: 24px;
}

input, button {
  border-radius: 12px !important;
  border: 2px solid #e2d2b5 !important;
  font-family: 'Fredoka', sans-serif !important;
}

button {
  background-color: #f59f0b !important;
  color: white !important;
}

.chat-box {
  background: #ffffff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
  max-width: 90%;
}
.message.right {
  flex-direction: row-reverse;
  margin-left: auto;
}

.avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid #ccc;
}

.bubble {
  padding: 12px 18px;
  border-radius: 16px;
  border: 2px solid rgba(0,0,0,0.05);
  font-size: 16px;
  box-shadow: inset -4px -4px 0px rgba(0,0,0,0.03);
  max-width: 70%;
}

.thinking .bubble {
  background: #f3f3f3 !important;
  color: #aaa !important;
  font-style: italic;
}

.vote-box {
  background: #fff6da;
  border-radius: 12px;
  padding: 16px;
  margin-top: 24px;
  border-left: 6px solid #f7c948;
  font-size: 16px;
  font-weight: 500;
  color: #6b4b00;
}
.vote-box ul {
  margin-top: 10px;
  padding-left: 20px;
}
.vote-box .final {
  margin-top: 16px;
  font-weight: bold;
  font-size: 18px;
  color: #4a2f00;
}
""") as demo:

    gr.Markdown("""<h1>🧠 你的脑内小会议</h1>""")
    with gr.Row():
        user_input = gr.Textbox(placeholder="例如：我该不该熬夜写论文？", label="你的纠结")
        submit = gr.Button("发言")

    html_output = gr.HTML("<div class='chat-box'></div>")

    submit.click(fn=run_debate, inputs=user_input, outputs=html_output)

if __name__ == '__main__':
    demo.launch()
