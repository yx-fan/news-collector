from django.test import TestCase
from .services.sentiment import analyze_sentiment

class SentimentAnalysisTest(TestCase):
    def test_positive_sentiment(self):
        text = "Tesla stock soars after record-breaking earnings report."
        print(text)
        sentiment_score = analyze_sentiment(text)
        self.assertGreater(sentiment_score, 0)
    
    def test_positive_sentiment_2(self):
        text = "Apple announces new product lineup, stock price rises."
        print(text)
        sentiment_score = analyze_sentiment(text)
        self.assertGreater(sentiment_score, 0)

    def test_negative_sentiment(self):
        text = "Apple faces backlash over controversial decision."
        print(text)
        sentiment_score = analyze_sentiment(text)
        self.assertLess(sentiment_score, 0)
    
    def test_negative_sentiment_2(self):
        text = "Tesla stock plummets after disappointing earnings report."
        print(text)
        sentiment_score = analyze_sentiment(text)
        self.assertLess(sentiment_score, 0)

    def test_neutral_sentiment(self):
        text = "nohting happened today"
        print(text)
        score = analyze_sentiment(text)
        self.assertAlmostEqual(score, 0, delta=0.2)
