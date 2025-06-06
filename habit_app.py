import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide")
st.title("🧠 Habit League Tracker")

# Step 1: User info
with st.form("user_info"):
    name = st.text_input("Name")
    if not name:
        st.warning("Name is required to proceed.")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    age = st.number_input("Age", min_value=10, max_value=100)
    location = st.text_input("Location")
    start_date = st.date_input("Start Date", min_value=datetime.date.today())
    duration = st.slider("League Duration (days)", 7, 60, 30)
    submit_user = st.form_submit_button("Find Goals")

if submit_user and name:
    first_name = name.split()[0]
    st.session_state["user_info"] = {
        "name": name,
        "first_name": first_name,
        "age": age,
        "location": location,
        "start_date": start_date,
        "duration": duration,
        "gender": gender
    }
    st.session_state["goals"] = [
        "Build Discipline",
        "Improve Focus",
        "Reduce Phone Usage",
        "Boost Fitness",
        "Healthy Lifestyle"
    ]
    st.success(f"Hi {first_name}, here are your AI-suggested goals.")

# Step 2: Select a goal and generate habits
if "goals" in st.session_state:
    selected_goal = st.selectbox("🎯 Select a goal to focus on", st.session_state["goals"])
    if st.button("Generate Habits"):
        st.session_state["selected_goal"] = selected_goal
        st.session_state["generate_habits_clicked"] = True

# Step 2.5: Load mock habits
if st.session_state.get("generate_habits_clicked", False):
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

    if st.button("Start League"):
        sorted_habits = sorted(habit_data, key=lambda x: x["difficulty"])
        st.session_state["selected_habits"] = sorted_habits[:6]
        st.success("Habits saved! League started!")

# Step 4: Calendar and Streak Tracker
if "selected_habits" in st.session_state:
    st.subheader("📅 Habit Calendar Tracker")
    start = st.session_state["user_info"]["start_date"]
    duration = st.session_state["user_info"]["duration"]
    days = [start + datetime.timedelta(days=i) for i in range(duration)]

    sorted_habits = st.session_state["selected_habits"]
    progress_df = pd.DataFrame(
        [[False]*len(days) for _ in sorted_habits],
        columns=[d.strftime("%Y-%m-%d") for d in days],
        index=[h["habit"] for h in sorted_habits]
    )

    edited_df = st.data_editor(
        progress_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=False,
        key="habit_tracker"
    )

    st.subheader("🔥 Streak Summary")
    habit_streaks = {}
    streak_days = 0
    for date in edited_df.columns:
        completed = edited_df[date].sum()
        if completed >= 4:
            streak_days += 1
    st.markdown(f"**🏆 Days with 4+ habits completed:** {streak_days} / {duration}")

    for habit in edited_df.index:
        streak = 0
        max_streak = 0
        for val in edited_df.loc[habit]:
            if val:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        habit_streaks[habit] = max_streak

    for habit, streak in habit_streaks.items():
        st.markdown(f"✅ {habit}: {streak} day streak")
