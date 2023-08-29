import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nrclex import NRCLex
from statistics import mean

# Download VADER lexicon
nltk.download('vader_lexicon')
nltk.download('punkt')


def analyze_sentiment_vader(text):
    vader_analyzer = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)
    scores = {'neg': [], 'neu': [], 'pos': [], 'compound': []}

    for sentence in sentences:
        sentiment = vader_analyzer.polarity_scores(sentence)
        for key in scores.keys():
            scores[key].append(sentiment[key])

    avg_scores = {key: mean(scores[key]) for key in scores.keys()}
    return [avg_scores['neg'], avg_scores['neu'], avg_scores['pos'], avg_scores['compound']]


def analyze_emotion_nrc(text):
    sentences = nltk.sent_tokenize(text)
    emotions_sum = {'anger': 0, 'anticip': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0, 'positive': 0,
                    'sadness': 0, 'surprise': 0, 'trust': 0}

    for sentence in sentences:
        emotion = NRCLex(sentence).affect_frequencies
        for key in emotions_sum.keys():
            if key in emotion:
                emotions_sum[key] += emotion[key]

    num_sentences = len(sentences)
    avg_emotions = {key: emotions_sum[key] / num_sentences for key in emotions_sum.keys()}
    return [avg_emotions[e] for e in
            ('anger', 'anticip', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust')]


def main():
    example_text1 = "I love this product. It has changed my life for the better!"
    example_text2 = "I’m so sorry this crazy man let loose on you. I get nervous around people like that for sure. He’s a f’ing coward and abuser of women."
    example_text3 = "I was screamed at by some right wing psycho in Costco yesterday while waiting for ice cream with my five year old."

    vader_result1 = analyze_sentiment_vader(example_text1)
    vader_result2 = analyze_sentiment_vader(example_text2)
    vader_result3 = analyze_sentiment_vader(example_text3)

    nrc_result1 = analyze_emotion_nrc(example_text1)
    nrc_result2 = analyze_emotion_nrc(example_text2)
    nrc_result3 = analyze_emotion_nrc(example_text3)

    print(f"Example Text 1 - VADER: {vader_result1}")
    print(f"Example Text 1 - NRC: {nrc_result1}")

    print(f"Example Text 2 - VADER: {vader_result2}")
    print(f"Example Text 2 - NRC: {nrc_result2}")

    print(f"Example Text 3 - VADER: {vader_result3}")
    print(f"Example Text 3 - NRC: {nrc_result3}")


if __name__ == "__main__":
    main()
