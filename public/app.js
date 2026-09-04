const form = document.querySelector('#chat-form');
const promptInput = document.querySelector('#prompt');
const messagesElement = document.querySelector('#messages');
const sendButton = document.querySelector('#send-button');
const clearButton = document.querySelector('#clear-button');
let messages = JSON.parse(localStorage.getItem('claudemind-messages') || '[]');

function renderMessage(role, content) {
  const wrapper = document.createElement('div');
  wrapper.className = 'message';
  const avatar = document.createElement('div');
  avatar.className = `avatar ${role === 'user' ? 'user-avatar' : 'assistant-avatar'}`;
  avatar.textContent = role === 'user' ? 'V' : 'C';
  const body = document.createElement('div');
  body.className = 'message-content';
  const author = document.createElement('strong');
  author.textContent = role === 'user' ? 'Voce' : 'ClaudeMind';
  const text = document.createElement('p');
  text.textContent = content;
  body.append(author, text);
  wrapper.append(avatar, body);
  messagesElement.append(wrapper);
}

function renderHistory() {
  messagesElement.innerHTML = '';
  messages.forEach((message) => renderMessage(message.role, message.content));
  messagesElement.scrollTop = messagesElement.scrollHeight;
}

function saveHistory() { localStorage.setItem('claudemind-messages', JSON.stringify(messages)); }

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const content = promptInput.value.trim();
  if (!content || sendButton.disabled) return;
  messages.push({ role: 'user', content });
  renderHistory();
  saveHistory();
  promptInput.value = '';
  sendButton.disabled = true;
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Nao foi possivel obter uma resposta.');
    messages.push({ role: 'assistant', content: data.message });
    renderHistory();
    saveHistory();
  } catch (error) {
    renderMessage('assistant', error.message);
  } finally { sendButton.disabled = false; promptInput.focus(); }
});

clearButton.addEventListener('click', () => { messages = []; saveHistory(); renderHistory(); });
promptInput.addEventListener('input', () => { promptInput.style.height = 'auto'; promptInput.style.height = `${Math.min(promptInput.scrollHeight, 130)}px`; });
renderHistory();
