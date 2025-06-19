from textblob import TextBlob
import re

def analyze_sentiment(text):
    if not text:
        return {
            'score': 0.0,
            'label': 'neutral'
        }
    
    # Convert to lowercase
    text = text.lower()
    
    # Define negative words and phrases
    negative_patterns = [
        'hate', 'terrible', 'awful', 'horrible', 'bad', 'worst',
        'useless', 'waste', 'poor', 'disappointed', 'disappointing',
        'not good', 'not great', 'not working', 'doesn\'t work',
        'broken', 'failure', 'fails', 'annoying', 'frustrating'
    ]
    
    # Check for negative patterns
    negative_count = sum(1 for pattern in negative_patterns if pattern in text)
    
    # Get TextBlob sentiment
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Adjust score based on negative patterns
    if negative_count > 0:
        # Increase negative sentiment weight
        polarity = polarity - (0.2 * negative_count)
    
    # Ensure score stays within -1 to 1 range
    final_score = max(min(polarity, 1.0), -1.0)
    
    # Determine label with adjusted thresholds
    if final_score < -0.1:
        label = 'negative'
    elif final_score > 0.1:
        label = 'positive'
    else:
        label = 'neutral'
    
    return {
        'score': final_score,
        'label': label,
        'details': {
            'negative_patterns_found': negative_count,
            'original_polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    }
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('sentiment/vader_lexicon.zip')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Join tokens back into text
    return ' '.join(tokens)

def analyze_sentiment(text):
    if not text:
        return {
            'score': 0.0,
            'label': 'neutral',
            'confidence': 0.0,
            'detailed_scores': None
        }
    # Check for special characters and replace them
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove any non-ASCII characters
    text = ''.join(char for char in text if ord(char) < 128)

    # Preprocess the text
    processed_text = preprocess_text(text)
    
    # Initialize analyzers
    sia = SentimentIntensityAnalyzer()
    
    # Get VADER sentiment scores
    vader_scores = sia.polarity_scores(text)  # Use original text for VADER
    
    # Get TextBlob sentiment
    blob = TextBlob(processed_text)
    textblob_polarity = blob.sentiment.polarity
    textblob_subjectivity = blob.sentiment.subjectivity
    
    # Combine scores (weighted average)
    compound_score = vader_scores['compound']
    final_score = (compound_score + textblob_polarity) / 2
    
    # Determine label and confidence
    if final_score > 0.2:
        label = 'positive'
        confidence = min(abs(final_score) * 1.5, 1.0)
    elif final_score < -0.2:
        label = 'negative'
        confidence = min(abs(final_score) * 1.5, 1.0)
    else:
        label = 'neutral'
        confidence = 1.0 - min(abs(final_score) * 2, 0.8)

    # Prepare detailed scores
    detailed_scores = {
        'vader': {
            'positive': vader_scores['pos'],
            'negative': vader_scores['neg'],
            'neutral': vader_scores['neu'],
            'compound': vader_scores['compound']
        },
        'textblob': {
            'polarity': textblob_polarity,
            'subjectivity': textblob_subjectivity
        }
    }

    return {
        'score': final_score,
        'label': label,
        'confidence': confidence,
        'detailed_scores': detailed_scores
    }

def get_emotion_keywords(text, label):
    """Extract emotion-related keywords based on sentiment"""
    processed_text = preprocess_text(text)
    blob = TextBlob(processed_text)
    
    # Get word sentiments
    word_sentiments = []
    for word in blob.words:
        word_blob = TextBlob(word)
        sentiment = word_blob.sentiment.polarity
        if abs(sentiment) > 0.3:  # Only include words with strong sentiment
            word_sentiments.append((word, sentiment))
    
    # Sort by absolute sentiment value
    word_sentiments.sort(key=lambda x: abs(x[1]), reverse=True)
    
    return [word for word, _ in word_sentiments[:5]]  # Return top 5 emotional words