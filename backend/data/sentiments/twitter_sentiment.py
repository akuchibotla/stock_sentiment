from transformers import pipeline

from .sentiment import Sentiment

class TwitterSentiment(Sentiment):
	def __init__(
		self,
		task: str | None = None,
		# More details about model: https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis
		pipeline_model: str = 'finiteautomata/bertweet-base-sentiment-analysis',
		positive_key: str = 'POS',
		negative_key: str = 'NEG'):
		# TODO: It is not super clear here that tasks are favored over pipeline_models
		# and that you need to provide at least one of them.
 		self.sentiment_pipeline = pipeline(task) if task \
 			else pipeline(model=pipeline_model)
 		self.positive_key = positive_key
 		self.negative_key = negative_key

	def _compute_sentiment_score_for_tweet(self, tweet_content: str) -> float:
		sentiment = self.sentiment_pipeline(tweet_content)
		raw_score = sentiment[0]['score']
		label = sentiment[0]['label']

		if label == self.negative_key:
			return -raw_score
		elif label == self.positive_key:
			return raw_score
		return 0

	def compute_average_sentiment_score_for_content_list(
		self,
		content_list) -> float:
		return sum([self._compute_sentiment_score_for_tweet(content.get_content()) \
			for content in content_list])/len(content_list)
