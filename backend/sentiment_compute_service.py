import datetime

from .data.source_data import SourceData
from .data.twitter_source_data import TwitterSourceData

class SentimentComputeService:
	class DailySentiments:
		def __init__(self):
			self._daily_sentiments = dict()

		def add_sentiment(
			self,
			sentiment: float,
			day: datetime.datetime,
			source_name: str) -> None:
			if day not in self._daily_sentiments:
				self._daily_sentiments[day] = dict()
			self._daily_sentiments[day][source_name] = sentiment

		def get_sentiments(self):
			return self._daily_sentiments

		def get_sentiments_for_day(self, day: datetime):
			return self._daily_sentiments[day]

	def __init__(self, source_data_sources: list[SourceData]):
		self.source_data_sources = source_data_sources

	def compute_sentiment(
		self,
		ticker: str,
		start_date: datetime.datetime,
		end_date: datetime.datetime) -> DailySentiments:
		days = (end_date - start_date).days
		
		daily_sentiments = self.DailySentiments()
		for data_source in self.source_data_sources:
			for day in range(days):
				curr_date = start_date + datetime.timedelta(days=day)
				sentiment = data_source.get_sentiment(
					ticker=ticker, day=curr_date)
				daily_sentiments.add_sentiment(
					sentiment=sentiment,
					day=curr_date,
					source_name=data_source.get_name())

		return daily_sentiments

# Example usage of service.
def main():
	twitter_source_data = TwitterSourceData()
	service = SentimentComputeService(
		source_data_sources=[twitter_source_data])

if __name__ == '__main__':
	main()