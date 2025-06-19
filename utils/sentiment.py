from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re

# 📥 Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


# 🔧 Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation/digits
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    return ' '.join(tokens)


# 🧠 Main Sentiment Analysis Function
def analyze_sentiment(text):
    if not text:
        return {
            'score': 0.0,
            'label': 'neutral',
            'confidence': 0.0,
            'detailed_scores': None
        }

    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = ''.join(c for c in cleaned_text if ord(c) < 128)
    processed_text = preprocess_text(cleaned_text)

    # VADER
    sia = SentimentIntensityAnalyzer()
    vader_scores = sia.polarity_scores(text)  # Use raw text for VADER

    # TextBlob
    blob = TextBlob(processed_text)
    blob_polarity = blob.sentiment.polarity
    blob_subjectivity = blob.sentiment.subjectivity

    # Combine scores
    final_score = (vader_scores['compound'] + blob_polarity) / 2

    # Label logic
    if final_score > 0.2:
        label = 'positive'
        confidence = min(abs(final_score) * 1.5, 1.0)
    elif final_score < -0.2:
        label = 'negative'
        confidence = min(abs(final_score) * 1.5, 1.0)
    else:
        label = 'neutral'
        confidence = 1.0 - min(abs(final_score) * 2, 0.8)

    return {
        'score': final_score,
        'label': label,
        'confidence': round(confidence, 2),
        'detailed_scores': {
            'vader': vader_scores,
            'textblob': {
                'polarity': blob_polarity,
                'subjectivity': blob_subjectivity
            }
        }
    }


# 🎯 Extract Emotionally Charged Keywords
def get_emotion_keywords(text, label):
    processed_text = preprocess_text(text)
    blob = TextBlob(processed_text)

    word_sentiments = []
    for word in blob.words:
        word_blob = TextBlob(word)
        sentiment = word_blob.sentiment.polarity
        if abs(sentiment) > 0.3:
            word_sentiments.append((word, sentiment))

    word_sentiments.sort(key=lambda x: abs(x[1]), reverse=True)
    return [word for word, _ in word_sentiments[:5]]
