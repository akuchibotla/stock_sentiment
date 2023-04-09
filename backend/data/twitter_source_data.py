from .source_data import SourceData
from .scrapers.twitter_scraper import TwitterScraper
from .sentiments.twitter_sentiment import TwitterSentiment

class TwitterSourceData(SourceData):
	def __init__(self):
		super().__init__(
			scraper=TwitterScraper(),
			sentiment=TwitterSentiment(),
			name='Twitter')