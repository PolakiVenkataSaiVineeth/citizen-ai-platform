# streamlit_app.py (converted from Flask)
import streamlit as st
from utils.sentiment import analyze_sentiment
from utils.nlu_handler import process_nlu
from datetime import datetime
import json
import os

# Set up data directory
DATA_DIR = 'data'
FEEDBACK_FILE = os.path.join(DATA_DIR, 'feedback.json')
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Citizen AI – Engagement Platform")
st.title("🧠 Citizen AI – Intelligent Engagement Platform")

# Navigation
page = st.sidebar.selectbox("Go to", ["Home", "Dashboard"])

if page == "Home":
    st.header("📬 Submit Your Feedback")
    feedback_text = st.text_area("Enter your feedback or question:")

    if st.button("Submit Feedback"):
        if not feedback_text:
            st.error("Please enter some feedback.")
        else:
            sentiment = analyze_sentiment(feedback_text)
            nlu_results = process_nlu(feedback_text)

            feedback_data = {
                'text': feedback_text,
                'sentiment': sentiment,
                'nlu_results': nlu_results,
                'timestamp': datetime.now().isoformat()
            }

            try:
                try:
                    with open(FEEDBACK_FILE, 'r') as f:
                        feedbacks = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    feedbacks = []

                feedbacks.append(feedback_data)

                with open(FEEDBACK_FILE, 'w') as f:
                    json.dump(feedbacks, f, indent=4)

                st.success("✅ Feedback submitted successfully!")
                st.json(feedback_data)
            except Exception as e:
                st.error(f"❌ Error saving feedback: {e}")

elif page == "Dashboard":
    st.header("📊 Citizen Feedback Dashboard")

    try:
        with open(FEEDBACK_FILE, 'r') as f:
            feedbacks = json.load(f)
        sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

        for entry in feedbacks:
            sentiments[entry['sentiment']] += 1

        st.subheader("Sentiment Distribution")
        st.bar_chart(sentiments)

        st.subheader("Recent Feedback")
        for fb in reversed(feedbacks[-5:]):
            st.markdown(f"**📝 {fb['text']}**")
            st.markdown(f"Sentiment: `{fb['sentiment']}` | Time: {fb['timestamp']}")
            st.markdown("---")

    except Exception as e:
        st.warning("⚠️ No feedback data available or file is corrupted.")
