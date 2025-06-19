# streamlit_app.py — with correct nltk punkt fix
import nltk

# ✅ Force proper punkt handling without using punkt_tab
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')

import streamlit as st
import json
import os
from datetime import datetime
from utils.sentiment import analyze_sentiment
from utils.nlu_handler import process_nlu

# Data file path
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)
feedback_file = os.path.join(data_dir, 'feedback.json')

# Load feedback data
def load_feedback():
    try:
        with open(feedback_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save feedback entry
def save_feedback(feedback_data):
    feedbacks = load_feedback()
    feedbacks.append(feedback_data)
    with open(feedback_file, 'w') as f:
        json.dump(feedbacks, f, indent=4)

# Streamlit UI
st.set_page_config(page_title="Citizen AI", layout="wide")
st.title("🤖 Citizen AI – Intelligent Public Feedback")

menu = st.sidebar.radio("Navigation", ["Feedback Form", "Dashboard"])

if menu == "Feedback Form":
    st.header("📝 Submit Your Feedback")
    feedback_text = st.text_area("What would you like to share?", height=150)

    if st.button("Submit"):
        if not feedback_text.strip():
            st.warning("Please enter some feedback.")
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
                save_feedback(feedback_data)
                st.success("Feedback submitted successfully!")
                st.json(feedback_data)
            except Exception as e:
                st.error(f"Error saving feedback: {e}")

elif menu == "Dashboard":
    st.header("📊 Feedback Dashboard")
    feedbacks = load_feedback()

    if not feedbacks:
        st.info("No feedback submitted yet.")
    else:
        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame(feedbacks)
        df['sentiment_label'] = df['sentiment'].apply(lambda s: s['label'] if isinstance(s, dict) else s)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        sentiment_counts = df['sentiment_label'].value_counts()
        st.subheader("Sentiment Overview")
        st.bar_chart(sentiment_counts)

        st.subheader("Recent Feedback")
        st.dataframe(df[['timestamp', 'text', 'sentiment_label']].sort_values(by='timestamp', ascending=False))
