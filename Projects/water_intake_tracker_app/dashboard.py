import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Water Tracker", page_icon="💧")

# ------------------ UI HEADER ------------------
st.title("💧 AI Water Intake Tracker")
st.markdown("Track your daily hydration and get AI feedback")

# ------------------ USER INPUT ------------------
user_id = st.text_input("User ID", value="kartik")
intake_ml = st.number_input(
    "Water Intake (ml)",
    min_value=0,
    step=100
)

# ------------------ LOG INTAKE ------------------
if st.button("Log Water Intake 💦"):
    response = requests.post(
        f"{API_URL}/log-intake",
        json={
            "user_id": user_id,
            "intake_ml": intake_ml
        }
    )

    if response.status_code == 200:
        data = response.json()
        st.success(data["message"])
        st.write("🤖 **AI Feedback:**")
        st.info(data["ai_feedback"])
    else:
        st.error("Failed to log intake")

#if st.button("Show History"):
    response = requests.get(f"{API_URL}/history/{user_id}")
    data = response.json()

    history = data["history"]

    if len(history) == 0:
        st.warning("No data found for this user!")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(history)

        st.subheader("📜 Intake Table")
        st.dataframe(df)

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Group by date (sum daily intake)
        
        daily_summary = df.groupby("date")["intake_ml"].sum().reset_index()

        st.subheader("📊 Water Intake Graph")

        df = df.reset_index(drop=True)
        df["entry"] = df.index + 1
        df["cumulative_intake"] = df["intake_ml"].cumsum()
        st.line_chart(
            df.set_index("date")["intake_ml"]
        )
# 🔑 GROUP BY DATE (IMPORTANT FIX)
