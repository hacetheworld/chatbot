import json
from flask import Flask, request, jsonify
from fuzzywuzzy import process
from flask_cors import CORS

# Load predefined questions and answers
with open("qa_data.json", "r") as file:
    qa_data = json.load(file)

# Convert JSON structure into a single dictionary
qa_dict = {}
for category in qa_data.values():
    qa_dict.update(category)

# Flask web server
app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Function to find best matching question
def get_best_match(user_input):
    questions = list(qa_dict.keys())
    best_match, score = process.extractOne(user_input.lower(), questions)
    return best_match if score > 60 else None  # Threshold for match confidence

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    best_match = get_best_match(user_input)

    if best_match:
        response = qa_dict[best_match]
    else:
        response = "I'm not sure about that. Can you rephrase the question?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
