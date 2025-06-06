import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="Habit League", layout="centered")
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
    start_date = st.date_input("Select Habit League Start Date", min_value=datetime.date.today())
    duration_days = st.slider("League Duration (days)", 7, 60, 21)
    frequency_all = st.selectbox("Select Habit Frequency", ["Daily", "Weekly"])

    if st.button("Generate Habits"):
        st.session_state.update({
            "selected_goal": selected_goal,
            "start_date": start_date,
            "duration_days": duration_days,
            "frequency_all": frequency_all,
            "generate_habits_clicked": True
        })

# Step 3: Load mock habits
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

# Step 4: Rate and rank
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
            "frequency": st.session_state["frequency_all"]
        })

    if st.button("Start League"):
        # Sort habits by easiest
        sorted_habits = sorted(habit_data, key=lambda x: x["difficulty"])[:6]
        st.session_state["selected_habits"] = sorted_habits

        # Build calendar
        start = st.session_state["start_date"]
        duration = st.session_state["duration_days"]
        days = [start + datetime.timedelta(days=i) for i in range(duration)]

        progress_df = pd.DataFrame(
            [[False]*6 for _ in days],
            columns=[h["habit"] for h in sorted_habits],
            index=[d.strftime("%Y-%m-%d") for d in days]
        )
        st.session_state["progress_df"] = progress_df
        st.success("League started! Begin tracking below ⬇️")

# Step 5: Habit Calendar & Streak Tracker
if "progress_df" in st.session_state:
    st.subheader("📆 Habit Tracker")

    df = st.session_state["progress_df"]

    for i, date in enumerate(df.index):
        st.markdown(f"### {date}")
        cols = st.columns(6)
        completed_today = 0
        for j, habit in enumerate(df.columns):
            with cols[j]:
                checkbox = st.checkbox(habit, key=f"{date}_{habit}", value=df.iloc[i, j])
                df.iloc[i, j] = checkbox
                if checkbox:
                    completed_today += 1

        if completed_today >= 4:
            st.success(f"🎉 League Win for {date} - {completed_today}/6 habits done!")

    # Save progress
    st.download_button(
        label="💾 Download Progress",
        data=df.to_csv().encode("utf-8"),
        file_name="habit_progress.csv",
        mime="text/csv"
    )

    # Streak Calculation
    st.subheader("🔥 Longest Streaks")
    for habit in df.columns:
        streak = 0
        max_streak = 0
        for status in df[habit]:
            if status:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        st.markdown(f"**{habit}** → 🔥 {max_streak} days")
