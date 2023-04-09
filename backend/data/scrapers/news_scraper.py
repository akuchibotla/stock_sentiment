import datetime

from .scraper import Scraper, Content

# TODO: Add support for News API.
class News(Scraper):
	def __init__(self) -> None:
		pass

	def fetch_content_for_day(
		self,
		ticker: str,
		day: datetime.datetime) -> list[Content]:
		raise NotImplementedError