import streamlit as st
import requests
import datetime

st.title("🧠 Habit League Tracker")

# Step 1: User info
with st.form("user_info"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    location = st.text_input("Location")
    start_date = st.date_input("Start Date", min_value=datetime.date.today())
    submit_user = st.form_submit_button("Generate Goals")

if submit_user:
    with st.spinner("Talking to AI..."):
        response = requests.post(
            "https://habit-ai-backend.onrender.com/generate-goals",  # update if different
            json={"name": name, "age": age, "location": location}
        )
        if response.status_code == 200:
            goals = response.json()["goals"]
            st.session_state["goals"] = goals
            st.success("Goals generated successfully!")
        else:
            st.error("Failed to generate goals. Try again.")

# Step 2: Select a goal
if "goals" in st.session_state:
    selected_goal = st.selectbox("Select a goal to focus on", st.session_state["goals"])
    if st.button("Generate Habits"):
        with st.spinner("Fetching habits..."):
            resp = requests.post(
                "https://habit-ai-backend.onrender.com/generate-habits",
                json={"goal": selected_goal}
            )
            if resp.status_code == 200:
                habits = resp.json()["habits"]
                st.session_state["habits"] = habits
                st.success("Habits generated!")
            else:
                st.error("Error fetching habits.")

# Step 3: Rate and select habits
if "habits" in st.session_state:
    st.subheader("📝 Rate difficulty (1–5) and select frequency")
    habit_data = []
    for i, habit in enumerate(st.session_state["habits"]):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.markdown(habit)
        with col2:
            difficulty = st.slider(f"Difficulty {i+1}", 1, 5, key=f"diff_{i}")
        with col3:
            freq = st.selectbox("Frequency", ["Daily", "Weekly"], key=f"freq_{i}")
        habit_data.append({
            "habit": habit,
            "difficulty": difficulty,
            "frequency": freq
        })

    if st.button("Save Habits"):
        st.session_state["selected_habits"] = habit_data
        st.success("Habits saved! Calendar/streak view coming next.")

# Placeholder for streak/calendar view (to be built next)
