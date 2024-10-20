import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
from scipy.special import softmax

# Load FinBERT pre-trained model
MODEL = 'yiyanghkust/finbert-tone'
tokenizer = BertTokenizer.from_pretrained(MODEL)
model = BertForSequenceClassification.from_pretrained(MODEL)

# Scraping internet articles
def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.get_text() for para in paragraphs])
    return article_text

# URLs of competitors' articles (replace with actual URLs)
urls = [
    'https://www.marketsmojo.com/news/stock-recommendation/aditya-vision-downgraded-to-hold-by-marketsmojo-despite-strong-performance-282715',
    'https://www.dailyexcelsior.com/reliance-digital-announces-festival-of-electronics-sale/',
    'https://www.quora.com/What-are-the-reasons-not-to-buy-product-from-reliance-digital',
    'https://www.statista.com/statistics/1043831/india-net-worth-bajaj-electricals-ltd/',
    'https://theprint.in/ani-press-releases/poojara-telecom-to-establish-strong-presence-in-rajasthan-with-extensive-expansion/1683050/'
]

# Scrape each article
articles = [scrape_article(url) for url in urls]

# Preprocessing text for FinBERT
def preprocess_text(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
    return inputs

# Sentiment analysis function
def analyze_sentiment(article):
    inputs = preprocess_text(article)
    outputs = model(**inputs)
    logits = outputs.logits.detach().numpy()
    sentiment_probabilities = softmax(logits, axis=1)
    sentiments = ['positive', 'neutral', 'negative']
    sentiment_index = np.argmax(sentiment_probabilities, axis=1)
    sentiment = sentiments[sentiment_index[0]]
    return sentiment, sentiment_probabilities[0]

# Analyze sentiment for each article
for i, article in enumerate(articles):
    sentiment, probabilities = analyze_sentiment(article)
    print(f"Article {i+1}:")
    print(f"Sentiment: {sentiment}")
    print(f"Probabilities (Positive, Neutral, Negative): {probabilities}\n")
