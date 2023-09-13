import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from json import dumps
import numpy as np
from nrclex import NRCLex

# Initialize Sentiment Analyzer
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# Initialize Reddit API
reddit = praw.Reddit(
    client_id="f9DgbQ1jB6PmDBEDp0DYKA",
    client_secret="1yTlU0mWLg51wMh-Y6GAwE1Dhc4PQQ",
    user_agent="sentimentanalyzertest",
    username="FlippyTheRatMan",
    password="Dontforgetthistime12@",
)

def analyze_sentiment(text):

    sentences = nltk.sent_tokenize(text)
    compound_scores = []

    for sentence in sentences:
        sentiment = analyzer.polarity_scores(sentence)
        compound_scores.append(sentiment['compound'])

    avg_compound_score = np.mean(compound_scores)

    return avg_compound_score


def analyze_emotion_nrc(text):
    emotions_sum = {'anger': 0, 'anticip': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0, 'positive': 0,
                    'sadness': 0, 'surprise': 0, 'trust': 0}

    emotion = NRCLex(text).affect_frequencies

    for key in emotions_sum.keys():
        if key in emotion:
            emotions_sum[key] = emotion[key]

    return emotions_sum

def fetch_comments(subreddit_list):
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)
        for comment in subreddit.stream.comments(skip_existing=True):

            sentiment_score = analyze_sentiment(comment.body)
            emotion_scores = analyze_emotion_nrc(comment.body)

            # Debug: Print each emotion score for the current comment
            # print(f"Debug: Comment ID: {comment.id}")
            for emotion, score in emotion_scores.items():
                print(f"Debug: {emotion}: {score}")

            comment_json = {
                "id": comment.id,
                "name": comment.name,
                "author": comment.author.name if comment.author else "Deleted",
                "body": comment.body,
                "subreddit": comment.subreddit.display_name,
                "upvotes": comment.ups,
                "downvotes": comment.downs,
                "over_18": comment.over_18,
                "timestamp": comment.created_utc,
                "permalink": comment.permalink,
                "sentiment_score": sentiment_score
            }

            comment_json.update(emotion_scores)

            yield comment_json
