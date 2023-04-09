import re
import datetime

import snscrape.modules.twitter as sntwitter

from .scraper import Scraper, Content

class TwitterScraper(Scraper):
	def __init__(self) -> None:
		pass

	def _query_constructor(
		self,
		ticker: str,
		min_date: datetime.datetime,
		max_date: datetime.datetime,
		min_faves: int = 300) -> str:
		format_date = lambda date: (
			f'{date.year}-'
			f'{str(date.month).rjust(2, "0")}-'
			f'{str(date.day).rjust(2, "0")}')

		return (
			f'${ticker} min_faves:{min_faves} until:{format_date(max_date)} '
			f'since:{format_date(min_date)}')

	def fetch_content_for_day(
		self,
		ticker: str,
		day: datetime.datetime) -> list[Content]:
		return self._fetch_content_for_day(ticker=ticker, day=day)

	def _fetch_content_for_day(
		self,
		ticker: str,
		day: datetime.datetime,
		min_faves: int = 300,
		limit: int = 25) -> list[Content]:
		query = self._query_constructor(
			ticker=ticker,
			min_faves=min_faves,
			min_date=day,
			max_date=day + datetime.timedelta(days=1))

		raw_tweets = sntwitter.TwitterSearchScraper(query).get_items()

		tweets = list()
		for _ in range(limit):
			curr_tweet = next(raw_tweets, None)
			if not curr_tweet:
				break
			
			tweet_content_trunc = curr_tweet.rawContent[:127]
			tweets.append(Content(content=tweet_content_trunc, date=day))

		return tweets