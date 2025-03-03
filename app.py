from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Simple rule-based chatbot logic
def chatbot_response(user_message):
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "how are you": "I'm just a program, but I'm here to help you!",
        "bye": "Goodbye! Have a great day!",
    }
    return responses.get(user_message.lower(), "I'm sorry, I didn't understand that. Can you rephrase?")

# Route to serve the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please provide a message."}), 400
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
