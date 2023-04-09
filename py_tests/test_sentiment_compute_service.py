import unittest
from unittest.mock import call, MagicMock

import datetime

from context import backend
from backend.sentiment_compute_service import SentimentComputeService
from backend.data.source_data import SourceData
from backend.data.scrapers.scraper import Scraper
from backend.data.sentiments.sentiment import Sentiment

MOCK_SOURCE_NAME = 'Mock Source'

class TestSentimentComputeService(unittest.TestCase):
	@classmethod
	def setUp(cls):
		cls.mock_scraper = Scraper()
		cls.mock_sentiment = Sentiment()

		cls.mock_source_data = SourceData(
			scraper=cls.mock_scraper,
			sentiment=cls.mock_sentiment,
			name=MOCK_SOURCE_NAME)

		cls.mock_service = SentimentComputeService(
			source_data_sources=[cls.mock_source_data])

	def test_compute_sentiment(self):
		days = 3
		mock_average_sentiment_scores_for_content_list = [0.5, 0.2, 0.6]
		self.mock_sentiment.compute_average_sentiment_score_for_content_list = \
			MagicMock(side_effect=mock_average_sentiment_scores_for_content_list)

		mock_daily_content_list = ['Test' for i in range(3 * days)]
		self.mock_scraper.fetch_content_for_day = MagicMock(side_effect=mock_daily_content_list)

		start_date = datetime.datetime(2020, 5, 17)
		daily_sentiments = self.mock_service.compute_sentiment(
			ticker='MOCK',
			start_date=start_date,
			end_date=start_date + datetime.timedelta(days=days))

		expected = [
			call(ticker='MOCK', day=start_date),
			call(ticker='MOCK', day=start_date + datetime.timedelta(days=1)),
			call(ticker='MOCK', day=start_date + datetime.timedelta(days=2))]
		self.mock_scraper.fetch_content_for_day.assert_has_calls(expected, any_order=False)

		for i in range(days):
			curr_date = start_date + datetime.timedelta(days=i)
			curr_sentiment_value = daily_sentiments.get_sentiments_for_day(curr_date)[MOCK_SOURCE_NAME]
			assert(curr_sentiment_value == mock_average_sentiment_scores_for_content_list[i])

if __name__ == '__main__':
    unittest.main()