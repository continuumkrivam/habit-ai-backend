from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Home route to serve index.html (so Replit treats it as a web app)
@app.route("/")
def serve_home():
    return send_from_directory('.', 'index.html')


# Endpoint to generate AI-based goals
@app.route("/generate-goals", methods=["POST"])
def generate_goals():
    user_data = request.json
    prompt = f"""
    Suggest 3 self-improvement goals for a person with:
    Name: {user_data['name']}
    Age: {user_data['age']}
    Location: {user_data['location']}.
    Goals should be practical and trackable.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    goals = response.choices[0].message.content.strip().split('\n')
    return jsonify({"goals": goals})


# Endpoint to generate 10 habits for a given goal
@app.route("/generate-habits", methods=["POST"])
def generate_habits():
    goal = request.json["goal"]
    prompt = f"""
    Suggest a bundle of 10 daily or weekly habits to achieve the following goal:
    "{goal}". Keep them short and action-oriented.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    habits = response.choices[0].message.content.strip().split('\n')
    return jsonify({"habits": habits})


# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
