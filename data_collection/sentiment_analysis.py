import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(comment):
    sentiment = sia.polarity_scores(comment)
    return sentiment