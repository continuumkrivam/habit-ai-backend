from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def health_check():
    return "Habit AI Backend is running."

@app.route("/generate-goals", methods=["POST"])
def generate_goals():
    try:
        data = request.json

        name = data.get("name")
        age = data.get("age")
        location = data.get("location")

        # Validate input
        if not all([name, age, location]):
            return jsonify({"error": "Missing name, age, or location"}), 400

        prompt = (
            f"Suggest 3 meaningful and realistic personal development goals for a "
            f"{age}-year-old named {name} from {location}. Format the goals as a numbered list."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful habit coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        # Extract goals from AI response
        content = response.choices[0].message.content.strip()
        goals = [line.strip() for line in content.split("\n") if line.strip()]
        
        return jsonify({"goals": goals}), 200

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
