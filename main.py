from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Habit AI Backend is running"

@app.route("/generate-goals", methods=["POST"])
def generate_goals():
    try:
        data = request.get_json()
        name = data.get("name", "")
        age = data.get("age", "")
        location = data.get("location", "")

        prompt = (
            f"Suggest 3 personalized habit goals for a person named {name}, "
            f"{age} years old, living in {location}. Return them as a list."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        goal_text = response.choices[0].message["content"]
        goals = [line.strip("-• ") for line in goal_text.split("\n") if line.strip()]
        return jsonify({"goals": goals})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
