import os
from flask import Flask
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Modern Chat</title>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  height: 100vh;
  font-family: "Inter", "Segoe UI", sans-serif;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  display: flex;
  justify-content: center;
  align-items: center;
}

#app {
  width: 420px;
  height: 600px;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(18px);
  border-radius: 20px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header */
#header {
  padding: 18px;
  text-align: center;
  font-size: 20px;
  font-weight: 600;
  color: white;
  background: rgba(255,255,255,0.08);
}

/* Messages */
#messages {
  flex: 1;
  padding: 18px;
  overflow-y: auto;
}

.message {
  max-width: 75%;
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(255,255,255,0.85);
  color: #222;
  animation: fadeIn 0.2s ease-in;
}

.message .user {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 2px;
}

.message .time {
  font-size: 11px;
  opacity: 0.6;
  float: right;
}

.message .text {
  font-size: 14px;
  margin-top: 4px;
}

/* Input */
#input {
  display: flex;
  padding: 14px;
  background: rgba(255,255,255,0.08);
}

#text {
  flex: 1;
  padding: 12px 14px;
  border-radius: 12px;
  border: none;
  outline: none;
  font-size: 14px;
}

button {
  margin-left: 10px;
  padding: 12px 18px;
  border-radius: 12px;
  border: none;
  background: #4facfe;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>

<div id="app">
  <div id="header">💬 Modern Chat</div>
  <div id="messages"></div>
  <div id="input">
    <input id="text" placeholder="Type a message…" />
    <button onclick="send()">Send</button>
  </div>
</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
const socket = io();
const messages = document.getElementById("messages");
const text = document.getElementById("text");

let username = "";
while (!username) {
  username = prompt("Choose a username");
}

function send() {
  if (text.value.trim()) {
    socket.emit("chat", {
      user: username,
      msg: text.value
    });
    text.value = "";
  }
}

socket.on("chat", data => {
  const div = document.createElement("div");
  div.className = "message";

  div.innerHTML = `
    <div class="user">
      ${data.user}
      <span class="time">${data.time}</span>
    </div>
    <div class="text">${data.msg}</div>
  `;

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
});
</script>

</body>
</html>
"""

@socketio.on("chat")
def chat(data):
    data["time"] = datetime.now().strftime("%H:%M")
    emit("chat", data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    socketio.run(app, host="0.0.0.0", port=port)



