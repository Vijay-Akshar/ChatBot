//Mapping our elements to this JS doc
const chatbox = document.getElementById('chatbox'); 
const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send');

function appendMessage(sender, text) { //Prints the message in the chat
  const msg = `${sender}: ${text}\n\n`;
  chatbox.textContent += msg;
  chatbox.scrollTop = chatbox.scrollHeight; //Scrolls to latest message
}

sendButton.onclick = async () => { //This says to the browser that something might make it freeze here, and to slow down the process instead.
  const msg = messageInput.value.trim();
  if (!msg) return;

  appendMessage("You", msg);
  messageInput.value = ""; //Resets the input to allow for more questions

  const res = await fetch("/ask", { //Slows the browser as we used async
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json(); //Again, slows the browser
  appendMessage("Bot", data.answer);
};

// 🔥 Press Enter to Send
messageInput.addEventListener("keydown", (e) => { //Press enter to send
  if (e.key === "Enter") {
    sendButton.click();
    e.preventDefault();
  }
});
