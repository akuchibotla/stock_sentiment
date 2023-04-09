import datetime

class Content():
	def __init__(self, content: str, date: datetime.datetime):
		self._content = content
		self._date = datetime.datetime

	def get_content(self):
		return self._content

	def get_date(self):
		return self._date

# Interface type class.
class Scraper:
	def fetch_content_for_day(
		self,
		ticker: str,
		day: datetime.datetime) -> list[Content]:
		raise NotImplementedError