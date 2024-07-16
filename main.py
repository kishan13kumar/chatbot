
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Set your API key
genai.configure(api_key="AIzaSyDbIBKiFwX4RI_zmUgK3jENjEVYkan995Y")

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #121212;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 90%;
            max-width: 600px;
            background-color: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: 80%;
        }
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 10px;
            margin-bottom: 10px;
            background-color: #2e2e2e;
        }
        .message {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #ff8c00;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #3a3a3a;
            align-self: flex-start;
        }
        .message-box {
            display: flex;
        }
        .message-box input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin-right: 10px;
            font-size: 16px;
            background-color: #2e2e2e;
            color: #ffffff;
        }
        .message-box button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #ff8c00;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
        }
        .message-box button:hover {
            background-color: #ffa500;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>Chat with our Bot</h1>
        <div id="chat-box" class="chat-box"></div>
        <div class="message-box">
            <input type="text" id="user-input" placeholder="Type your message here..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(text, className) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            if (userInput.trim() === '') return;
            addMessage(userInput, 'user-message');
            document.getElementById('user-input').value = '';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'message=' + encodeURIComponent(userInput)
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'bot-message');
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/chat", methods=["POST"])
def chat_response():
    user_message = request.form["message"]
    response = chat.send_message(user_message)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
