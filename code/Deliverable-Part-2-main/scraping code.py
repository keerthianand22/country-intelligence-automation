import requests
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from serpapi import GoogleSearch


import nltk
nltk.download('punkt_tab')

#  Setup NLP tools
analyzer = SentimentIntensityAnalyzer()
sentiment_pipeline = pipeline("sentiment-analysis", batch_size=8)

#  URLs to scrape
URLS = [
    'https://www.defensenews.com/',
    'https://www.twz.com/',
    'https://www.nato.int/',
    'https://www.cia.gov/',
    'https://www.globalfirepower.com/',
    'https://defence24.com/',
    'https://www.popularmechanics.com/',
    'https://www.worldometers.info/',
    'https://ourworldindata.org/',
    'https://www.cia.gov/the-world-factbook/countries/',
    'https://www.climatestotravel.com/',
    'https://www.trade.gov/country-commercial-guides/',
    'https://www.statista.com/statistics/',
    'https://www.imf.org/external/datamapper/',
    'https://trendeconomy.com/data/',
    'https://www.eia.gov/international/overview/world'
]

#  G20 Countries
G20_COUNTRIES = [
    "Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", "India", "Indonesia",
    "Italy", "Japan", "Mexico", "Russia", "Saudi Arabia", "South Africa", "South Korea", "Turkey", "United Kingdom",
    "United States", "European Union"
]

#  Function to fetch page content with retry & exponential backoff
def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    delay = 5
    for _ in range(5):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                print(f"⚠️ Rate limited at {url}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
                continue
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    return None

#  Function to extract article content safely
def extract_article_content(article_url):
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        date = article.publish_date if article.publish_date else "Unknown"
        summary = summarize_article(article.text)
        return article.title, article.text[:1000], summary, date
    except Exception as e:
        print(f"⚠️ Skipping {article_url} due to error: {e}")
        return None, None, None, None

#  Function to summarize an article
def summarize_article(text, num_sentences=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        print(f"⚠️ Error summarizing article: {e}")
        return "Summary not available"

#  Function to analyze sentiment
def analyze_sentiment(text):
    vader_score = analyzer.polarity_scores(text)['compound']
    bert_result = sentiment_pipeline([text])[0]
    bert_score = bert_result['score'] if bert_result['label'] == "POSITIVE" else -bert_result['score']
    final_score = (vader_score + bert_score) / 2
    sentiment = "Positive" if final_score > 0.05 else "Negative" if final_score < -0.05 else "Neutral"
    return final_score, sentiment

#  Function to determine impacted country
def identify_country(text):
    for country in G20_COUNTRIES:
        if country.lower() in text.lower():
            return country
    return "Unknown"

#  Function to scrape articles
def scrape_articles():
    all_articles = []
    for url in URLS:
        print(f"🔍 Scraping {url}...")
        html = fetch_page(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                article_url = urljoin(url, link['href'])
                if article_url.startswith("javascript:"):
                    continue
                title, text, summary, date = extract_article_content(article_url)
                if not title or not text:
                    continue
                sentiment_score, sentiment = analyze_sentiment(text)
                country = identify_country(text)
                all_articles.append({
                    'Title': title,
                    'Link': article_url,
                    'Summary': summary,
                    'Date': date,
                    'Sentiment Score': sentiment_score,
                    'Sentiment': sentiment,
                    'Country': country,
                    'Impact on Country': "Likely Positive" if sentiment_score > 0 else "Likely Negative" if sentiment_score < 0 else "Neutral"
                })
                time.sleep(random.uniform(3, 6))
    return all_articles

#  Function to search Google and extract articles
def search_google_articles():
    all_articles = []
    for country in G20_COUNTRIES:
        query = f"{country} defense news latest"
        search_params = {"q": query, "api_key": "5db731eb044cd4f812750918d14c186b7b25e70ab32b6e3f621fb59d57fcdda6"}
        search_results = GoogleSearch(search_params).get_dict()
        for result in search_results.get("organic_results", []):
            article_url = result["link"]
            title, text, summary, date = extract_article_content(article_url)
            if not title or not text:
                continue
            sentiment_score, sentiment = analyze_sentiment(text)
            all_articles.append({
                'Title': title,
                'Link': article_url,
                'Summary': summary,
                'Date': date,
                'Sentiment Score': sentiment_score,
                'Sentiment': sentiment,
                'Country': country,
                'Impact on Country': "Likely Positive" if sentiment_score > 0 else "Likely Negative" if sentiment_score < 0 else "Neutral"
            })
    return all_articles

#  Run scraping and save results
all_articles = scrape_articles() + search_google_articles()
pd.DataFrame(all_articles).to_csv('Defense_Analysis2.csv', index=False)
print(f" Saved {len(all_articles)} articles.")
