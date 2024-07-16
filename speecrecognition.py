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
    <title>KI Bot</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f7f9fc;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 90%;
            max-width: 800px;
            height: 90vh;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .chat-header {
            background-color: #4a90e2;
            color: #fff;
            padding: 15px;
            text-align: center;
            font-size: 1.5em;
            font-weight: 500;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        }
        .chat-box {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #eef1f6;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            position: relative;
            padding: 12px 40px 12px 20px;
            border-radius: 25px;
            word-wrap: break-word;
            max-width: 70%;
            display: inline-block;
            clear: both;
            font-size: 0.9em;
        }
        .user-message {
            background-color: #4a90e2;
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 0;
        }
        .ki-bot-message {
            background-color: #fff;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .copy-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            right: 10px;
            background-color: transparent;
            border: none;
            color: #4a90e2;
            cursor: pointer;
        }
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .feedback-btn {
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8em;
        }
        .good-btn {
            background-color: transparent;
            color: #4caf50;
        }
        .bad-btn {
            background-color: transparent;
            color: #f44336;
        }
        .message-box {
            display: flex;
            padding: 10px 20px;
            border-top: 1px solid #ddd;
            background-color: #fff;
            align-items: center;
        }
        .message-box input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            margin-right: 10px;
        }
        .message-box button {
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            background-color: #4a90e2;
            color: #fff;
            font-size: 1em;
            cursor: pointer;
            transition: background-color 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .message-box button:hover {
            background-color: #357ab8;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4a90e2;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 2s linear infinite;
            display: none;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @media only screen and (max-width: 600px) {
            .chat-container {
                width: 100%;
                height: 100vh;
                border-radius: 0;
            }
            .chat-header {
                font-size: 1.2em;
                padding: 10px;
            }
            .message-box input[type="text"] {
                font-size: 0.9em;
            }
            .message-box button {
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">KI Bot</div>
        <div id="chat-box" class="chat-box"></div>
        <div class="message-box">
            <input type="text" id="user-input" placeholder="Type your message here..." />
            <button onclick="sendMessage()"><i class="fas fa-rocket"></i></button>
            <div class="loader"></div>
        </div>
    </div>

    <script>
        function addMessage(text, className) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = text;

            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.onclick = () => copyToClipboard(text);

            messageDiv.appendChild(copyBtn);

            if (className === 'ki-bot-message') {
                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'feedback-buttons';

                const goodBtn = document.createElement('button');
                goodBtn.className = 'feedback-btn good-btn';
                goodBtn.innerHTML = '<i class="fas fa-thumbs-up"></i>';
                goodBtn.onclick = () => sendFeedback(text, 'good');

                const badBtn = document.createElement('button');
                badBtn.className = 'feedback-btn bad-btn';
                badBtn.innerHTML = '<i class="fas fa-thumbs-down"></i>';
                badBtn.onclick = () => sendFeedback(text, 'bad');

                feedbackDiv.appendChild(goodBtn);
                feedbackDiv.appendChild(badBtn);

                messageDiv.appendChild(feedbackDiv);
            }

            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Message copied to clipboard');
            }, () => {
                alert('Failed to copy message');
            });
        }

        function sendFeedback(message, feedback) {
            fetch('/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, feedback: feedback })
            }).then(response => response.json())
              .then(data => {
                  alert('Feedback submitted: ' + data.status);
              });
        }

        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            if (userInput.trim() === '') return;
            addMessage(userInput, 'user-message');
            document.getElementById('user-input').value = '';

            const loader = document.querySelector('.loader');
            loader.style.display = 'block';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'message=' + encodeURIComponent(userInput)
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'ki-bot-message');
                loader.style.display = 'none';
            });
        }

        document.getElementById('user-input').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        document.getElementById('user-input').focus();
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

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    message = data.get("message")
    feedback = data.get("feedback")
    # Here, you can log the feedback to a database or a file
    print(f"Feedback received: {feedback} for message: {message}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
