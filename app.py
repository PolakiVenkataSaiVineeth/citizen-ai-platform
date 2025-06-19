from flask import Flask, render_template, request, jsonify
from utils.sentiment import analyze_sentiment
from utils.nlu_handler import process_nlu
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback_text = data.get('feedback')
    
    if not feedback_text:
        return jsonify({'error': 'No feedback provided'}), 400
    
    # Analyze sentiment
    sentiment = analyze_sentiment(feedback_text)
    
    # Process with NLU
    nlu_results = process_nlu(feedback_text)
    
    # Combine results
    feedback_data = {
        'text': feedback_text,
        'sentiment': sentiment,
        'nlu_results': nlu_results,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save to JSON file
    try:
        save_feedback(feedback_data)
        return jsonify(feedback_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_feedback(feedback_data):
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    feedback_file = os.path.join(data_dir, 'feedback.json')
    
    try:
        with open(feedback_file, 'r') as f:
            feedbacks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        feedbacks = []
    
    feedbacks.append(feedback_data)
    
    with open(feedback_file, 'w') as f:
        json.dump(feedbacks, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
