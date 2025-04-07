const chatbox = document.getElementById('chatbox');
const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send');

function appendMessage(sender, text) {
  const msg = `${sender}: ${text}\n\n`;
  chatbox.textContent += msg;
  chatbox.scrollTop = chatbox.scrollHeight;
}

sendButton.onclick = async () => {
  const msg = messageInput.value.trim();
  if (!msg) return;

  appendMessage("You", msg);
  messageInput.value = "";

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json();
  appendMessage("Bot", data.answer);
};

// 🔥 Press Enter to Send
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendButton.click();
    e.preventDefault();
  }
});
