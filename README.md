# Sentiment Analysis

A tool that uses AI/ML to fetch social sentiments about various securities, by ticker. Service exposed via Flask API REST endpoints.

## Setup
Highly reccomend using a virtual environment, I wrote this with Python 3.11.3.
```
git clone git@github.com:akuchibotla/stock_sentiment.git

# Optional
pyenv activate

cd stock_sentiment
pip3 install -r requirements.txt
python -m flask --app backend/app run
```

## Usage
Here's an example request.
```
export TICKER=TSLA
export STARTDATE="2022-05-03"
export ENDDATE="2022-05-13"
curl -X GET 'http://127.0.0.1:5000/v1/sentiment?ticker='${TICKER}'&startDate='${STARTDATE}'&endDate='${ENDDATE}''
```
Response (currently only supports Twitter, but can support other information sources easily)
```
[
	{
		"date": "2022-05-03",
		"data": {
			"Twitter": 0.10201783974965413
		}
	}, 
	{
		"date": "2022-05-04",
		"data": {
			"Twitter": -0.08599245861956947
		}
	}, 
	{
		"date": "2022-05-05",
		"data": {
			"Twitter": 0.02721612608951071
		}
	}, 
	{
		"date": "2022-05-06",
		"data": {
			"Twitter": 0.16234786259500603
		}
	}, 
	{
		"date": "2022-05-07",
		"data": {
			"Twitter": 0.15962315909564495
		}
	}, 
	{
		"date": "2022-05-08",
		"data": {
			"Twitter": 0.2275254726409912
		}
	}, 
	{
		"date": "2022-05-09",
		"data": {
			"Twitter": 0.1808691954612732
		}
	}, 
	{
		"date": "2022-05-10",
		"data": {
			"Twitter": 0.09536484479904175
		}
	}, 
	{
		"date": "2022-05-11",
		"data": {
			"Twitter": 0.10376882314682007
		}
	}, 
	{
		"date": "2022-05-12",
		"data": {
			"Twitter": 0.037416250705718995
		}
	}
]
```

## Features
* Flask API makes it convenient to port over to front ends.
* Can specify tickers and a date range, to understand how sentiment changes over time.
* Supports Twitter today, but is easily extensible to other social media apps and news sources.
  * By default uses a BERT model trained specifically on Tweets, but there is model extensibility to choose custom models for different contexts.
  * Has some pre-set configurations to ensure that high-value content is being considered (minimum number of favorites on the Tweet). Can make this even more customizable.

## Future Improvements
* Normalize sentiment values, right now they don't really mean anything and can vary based on model.
* Correlate to company name and search for content there as well, rather than just the ticker. Lot of great content is out there referencing company names rather than tickers.
* Integrate with Reddit, news API, etc.
* Add support for cryptocurrencies.
* Consider sector wide news as well, with some weightage: sector funds, competitors, etc.
* Use a real dependency injection framework.
* Likely need to add some comments for clarity.
* Much more testing needed.
* Validate tickers.

## Limitations
* It is god-awfully slow, likely due to scraper or AI model size.
* Scraper is a backdoor integration to social sites, unsure what maintenance looks like long term.
* Unfit for a Heroku deploy because slug size is too big (500 MB max, 2.2 GB currently), either BERT model or HuggingFace pipeline is too large.