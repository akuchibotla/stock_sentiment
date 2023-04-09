import datetime

from flask import Flask, request, make_response
from flask_api import status
from flask_parameter_validation import ValidateParameters, Query

from .data.twitter_source_data import TwitterSourceData
from .sentiment_compute_service import SentimentComputeService

twitter_source_data = TwitterSourceData()
sentiment_compute_service = SentimentComputeService(
	source_data_sources=[twitter_source_data])

app = Flask(__name__)

def jsonify_daily_sentiments(sentiments):
	json_ready_sentiments = list()
	for date in sentiments:
		date_str = datetime.datetime.strftime(date, '%Y-%m-%d')
		curr_data = {
			'date': date_str,
			'data': sentiments[date].copy()
		}
		json_ready_sentiments.append(curr_data)

	return sorted(json_ready_sentiments, key=lambda data_node: data_node['date'])

def validate_and_convert_dates(start_date: str, end_date: str):
	start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

	if start_date_datetime >= end_date_datetime:
		return make_response(f'startDate {startDate} cannot be after or greater than endDate {endDate}.', status.HTTP_400_BAD_REQUEST)

	if start_date_datetime > datetime.datetime.now():
		return make_response(f'startDate {startDate} cannot be in the future {endDate}.', status.HTTP_400_BAD_REQUEST)

	return (start_date_datetime, end_date_datetime)

@app.route('/v1/sentiment', methods=['GET'])
@ValidateParameters()
def sentiment(
	ticker: str = Query(),
	startDate: str = Query(pattern=r'^\d{4}-\d{2}-\d{2}$'),
	endDate: str = Query(pattern=r'^\d{4}-\d{2}-\d{2}$')):
	start_date_datetime, end_date_datetime = validate_and_convert_dates(startDate, endDate)
	daily_sentiments = sentiment_compute_service.compute_sentiment(
		ticker=ticker,
		start_date=start_date_datetime,
		end_date=end_date_datetime)

	return jsonify_daily_sentiments(daily_sentiments.get_sentiments())