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

  // 渲染发言（多轮兼容）
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

  // 渲染投票信息（大改版）
  const voteHTML = `
  <div class="vote-header">📊 最终投票：</div>
  <div class="vote-grid">
    ${data.votes.map(v => `
      <div class="vote-mini-card">
        <div class="vote-role">${v.name}</div>
        <div class="vote-bar emotion"><div class="vote-bar-inner" style="width:${v.emotion * 100}%"></div></div>
        <div class="vote-bar logic"><div class="vote-bar-inner" style="width:${v.logic * 100}%"></div></div>
        <div class="vote-mini-score">🧮 ${v.weight.toFixed(2)}</div>
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
