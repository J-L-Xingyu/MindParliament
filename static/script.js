document.getElementById('submitBtn').addEventListener('click', async () => {
  const input = document.getElementById('problemInput');
  const chatWindow = document.getElementById('chatWindow');
  const voteWindow = document.getElementById('voteWindow');

  const problem = input.value.trim();
  if (!problem) return;

  input.disabled = true;
  chatWindow.innerHTML = '<p>⏳ 正在召集脑内小会议...</p>';
  voteWindow.innerHTML = '';

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem })
  });

  const data = await res.json();
  chatWindow.innerHTML = '';

  // 渲染发言 + 打字效果
  for (let i = 0; i < data.messages.length; i++) {
    const msg = data.messages[i];
    const side = i % 2 === 1 ? 'right' : 'left';
    const avatar = `/static/avatars/${msg.name.toLowerCase()}.png`;
    const bubbleClass = `bubble ${msg.name.toLowerCase()}`;

    const msgElem = document.createElement('div');
    msgElem.className = `message ${side}`;
    msgElem.innerHTML = `
      <div class="avatar"><img src="${avatar}" /></div>
      <div class="${bubbleClass}"></div>
    `;
    chatWindow.appendChild(msgElem);

    const bubble = msgElem.querySelector('.bubble');
    await typeText(bubble, msg.opinion);
  }

  // 渲染投票信息
  const voteHTML = `
    <div class="vote-header">📊 最终投票：</div>
    <div class="vote-list">
      ${data.votes.map(v => `
        <div class="vote-card ${v.name.toLowerCase()}">
          <div class="vote-title">${v.name}</div>
          <div class="vote-bar">
            <div class="vote-bar-inner" style="width:${v.weight * 25}px"></div>
          </div>
          <div class="vote-score">情绪 ${v.emotion} × 理性 ${v.logic} = <b>${v.weight}</b></div>
        </div>
      `).join('')}
    </div>
    <div class="final">🔚 综合建议：<strong>${data.suggestion}</strong></div>
  `;
  voteWindow.innerHTML = voteHTML;

  input.disabled = false;
});

async function typeText(element, text) {
  element.textContent = '';
  for (let i = 0; i < text.length; i++) {
    element.textContent += text[i];
    await new Promise(r => setTimeout(r, 25));
  }
}