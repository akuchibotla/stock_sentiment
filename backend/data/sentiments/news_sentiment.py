from transformers import pipeline

from .sentiment import Sentiment

# TODO: Add support for News API.
class NewsSentiment(Sentiment):
	def __init__(self):
		raise NotImplementedError

	def compute_average_sentiment_score_for_content_list(
		self,
		content_list: list[str]) -> int:
		raise NotImplementedError
