import datetime

from .scrapers.scraper import Scraper
from .sentiments.sentiment import Sentiment

# Implementation type class.
# Bundles scraper and sentiment computation logic into one bundle for one data source. 
class SourceData:
	def __init__(self, scraper: Scraper, sentiment: Sentiment, name: str):
		self._scraper = scraper
		self._sentiment = sentiment
		self._name = name

	def get_sentiment(self, ticker: str, day: datetime.datetime) -> float:
		content = self._scraper.fetch_content_for_day(ticker=ticker, day=day)
		return self._sentiment.compute_average_sentiment_score_for_content_list(content)

	def get_name(self):
		return self._name