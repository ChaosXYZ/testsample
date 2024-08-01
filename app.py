from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    # This is where you'd implement your chatbot logic
    bot_response = generate_response(user_message)
    return jsonify({'response': bot_response})

def generate_response(message):
    # Simple response generation (replace with more sophisticated logic)
    return f"You said: {message}. This is a simple echo response."

if __name__ == '__main__':
    app.run(debug=True)
