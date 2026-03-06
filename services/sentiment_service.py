from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of a given text and returns 'happy', 'sad', or 'neutral'.
    """
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        return "happy"
    elif compound <= -0.05:
        return "sad"
    else:
        return "neutral"
