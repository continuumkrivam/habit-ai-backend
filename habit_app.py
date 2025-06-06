import streamlit as st
import datetime

st.title("🧠 Habit League Tracker")

# Step 1: User info
with st.form("user_info"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    location = st.text_input("Location")
    start_date = st.date_input("Start Date", min_value=datetime.date.today())
    submit_user = st.form_submit_button("Generate Goals")

# Mock goal generation
if submit_user:
    with st.spinner("Generating mock goals..."):
        goals = [
            "1. Improve daily focus with 1 hour of deep work",
            "2. Build strength through consistent workouts",
            "3. Enhance well-being with nightly journaling"
        ]
        st.session_state["goals"] = goals
        st.success("Mock goals loaded successfully!")

# Step 2: Select a goal
if "goals" in st.session_state:
    selected_goal = st.selectbox("Select a goal to focus on", st.session_state["goals"])
    if st.button("Generate Habits"):
        with st.spinner("Loading mock habits..."):
            habits = [
                "Read 10 pages of a book",
                "Journal for 5 minutes",
                "Walk for 20 minutes",
                "Plan next day in advance",
                "Do 15 push-ups",
                "Meditate for 10 minutes",
                "Stretch in the morning",
                "No screen after 9 PM",
                "Drink 2L water",
                "Eat 1 healthy meal"
            ]
            st.session_state["habits"] = habits
            st.success("Mock habits loaded successfully!")

# Step 3: Rate and select habits
if "habits" in st.session_state:
    st.subheader("📝 Rate difficulty (1–5) and select frequency")
