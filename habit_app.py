import streamlit as st
import datetime

st.title("🧠 Habit League Tracker")

# Step 1: User Info (name, age, location only)
with st.form("user_info"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    location = st.text_input("Location")
    submit_user = st.form_submit_button("Find Goals")

# Step 1.5: Generate mock goals
if submit_user:
    with st.spinner("Generating mock goals..."):
        goals = [
            "1. Improve daily focus with 1 hour of deep work",
            "2. Build strength through consistent workouts",
            "3. Enhance well-being with nightly journaling"
        ]
        st.session_state["goals"] = goals
        st.success("Mock goals loaded successfully!")

# Step 2: Show goals and capture Start Date + Frequency
if "goals" in st.session_state:
    selected_goal = st.selectbox("Select a goal to focus on", st.session_state["goals"])

    # New position for Start Date and Frequency
    start_date = st.date_input("Select Habit League Start Date", min_value=datetime.date.today())
    frequency_all = st.selectbox("Select Habit Frequency for League", ["Daily", "Weekly"])

    if st.button("Generate Habits"):
        st.session_state["selected_goal"] = selected_goal
        st.session_state["start_date"] = start_date
        st.session_state["frequency_all"] = frequency_all
        st.session_state["generate_habits_clicked"] = True

# Step 3: Generate mock habits if triggered
if st.session_state.get("generate_habits_clicked", False):
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
        st.session_state["generate_habits_clicked"] = False
        st.success("Mock habits loaded successfully!")

# Step 4: Rate and select habits
if "habits" in st.session_state:
    st.subheader("📝 Rate difficulty (1–5)")

    habit_data = []
    for i, habit in enumerate(st.session_state["habits"]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(habit)
        with col2:
            difficulty = st.slider(f"Difficulty {i+1}", 1, 5, key=f"diff_{i}")
        habit_data.append({
            "habit": habit,
            "difficulty": difficulty,
            "frequency": st.session_state.get("frequency_all", "Daily")
        })

    if st.button("Save Habits"):
        st.session_state["selected_habits"] = habit_data
        st.success("Habits saved! Calendar/streak view coming next.")
