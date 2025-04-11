import gradio as gr
import time
from agents.optimist import OptimistAgent
from agents.pessimist import PessimistAgent
from agents.realist import RealistAgent
from agents.alert import AlertAgent
from agents.strategist import StrategistAgent

AGENTS = [
    OptimistAgent(), PessimistAgent(), RealistAgent(), AlertAgent(), StrategistAgent()
]

IMG_URL = "file=images/joy.png"

COLORS = {
    "Optimist": "#fdf3dc",
    "Pessimist": "#dfeaf4",
    "Realist": "#eaeaea",
    "Alert": "#fce8e8",
    "Strategist": "#e5f7e1"
}

TEXT_COLORS = {
    "Optimist": "#5f4200",
    "Pessimist": "#1c3f5e",
    "Realist": "#333333",
    "Alert": "#7a1a1a",
    "Strategist": "#234c1e"
}

# 渲染图像风格角色对话气泡
def render_agent_message(agent, content):
    bg = COLORS[agent.name]
    fg = TEXT_COLORS[agent.name]
    return f"""
    <div class='bubble-box'>
        <img class='avatar-img' src='{IMG_URL}' />
        <div class='bubble' style='background:{bg}; color:{fg};'>
            {content}
        </div>
    </div>
    """

def run_debate(problem):
    all_opinions = []
    chat_html = "<div class='chat-window'>"

    for agent in AGENTS:
        yield chat_html + f"<div class='bubble-box thinking'><img class='avatar-img' src='{IMG_URL}' /><div class='bubble'>......</div></div></div>"
        time.sleep(0.8)
        agent.adjust_emotion(all_opinions)
        opinion = agent.respond(problem, all_opinions)
        all_opinions.append(opinion)
        chat_html += render_agent_message(agent, opinion)
        yield chat_html + "</div>"
        time.sleep(0.5)

    if sum(agent.vote_weight() * agent.evaluate_opinion(problem) for agent in AGENTS) > len(AGENTS) * 0.5:
        suggestion = "写吧！做就是了！🔥"
    else:
        suggestion = "建议等等，再好好想想～"

    chat_html += f"<div class='final-suggest'>建议：{suggestion}</div>"
    yield chat_html + "</div>"

with gr.Blocks(css="""
body { font-family: 'Inter', sans-serif; background: #fffaf3; }
.chat-window { border-radius: 16px; background: #fffdf8; padding: 24px; border: 2px solid #e8dcc9; }
.bubble-box { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; }
.avatar-img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #eee;
  border: 2px solid #ccc;
}
.bubble {
  border-radius: 16px;
  padding: 12px 18px;
  font-size: 15px;
  box-shadow: inset -4px -4px 0px rgba(0,0,0,0.05);
  border: 2px solid rgba(0,0,0,0.08);
  max-width: 80%;
}
.thinking .bubble { color: #999 !important; background: #f3f3f3 !important; font-style: italic; }
.final-suggest {
  margin-top: 24px;
  font-weight: bold;
  font-size: 18px;
  background: #fff3c7;
  border-left: 6px solid #ffbb33;
  padding: 12px 16px;
  border-radius: 10px;
  color: #4a2f00;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
}
""") as demo:

    gr.Markdown("""<h1 style='font-weight:900;font-size:28px;color:#5b3e1d;'>🧠 你的脑内小会议</h1>""")
    with gr.Row():
        user_input = gr.Textbox(placeholder="例如：我该不该写论文？", label="你的纠结")
        submit = gr.Button("发言")

    html_output = gr.HTML("<div class='chat-window'></div>")

    submit.click(fn=run_debate, inputs=user_input, outputs=html_output)

if __name__ == '__main__':
    demo.launch()
