from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Habit AI Backend is running"

@app.route("/generate-goals", methods=["POST"])
def generate_goals():
    try:
        data = request.get_json()
        name = data.get("name", "User")
        age = data.get("age", "30")
        location = data.get("location", "your city")

        prompt = (
            f"Suggest 3 personalized goals for a person named {name}, "
            f"{age} years old, living in {location}. Return the list only."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful habit coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        goal_text = response['choices'][0]['message']['content']
        goals = [line.strip("-•123. ") for line in goal_text.split('\n') if line.strip()]
        return jsonify({"goals": goals})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
