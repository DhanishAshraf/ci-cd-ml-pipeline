""" A simple example of how to query a model API that has been deployed using Flask.
To run: src/flask_app $ python query_model.py
This script assumes flask application is running. See flask_app/app.py for details.
"""


import requests, random, json
from pandas import read_csv

# URL of flask application
flask_app_url = 'http://0.0.0.0:8080'


def get_model_info():
	""" get deployed model's information
	
	Returns:
		result.text -- the returned json as text (because it prints nicer than as json)
	"""
	result = requests.get(flask_app_url)
	return result.text 


def classify_sample(data):
	""" Use the Flask app's POST method to make a classification using the model 

	Keyword arguments:
	data -- the data to be classified in padas dataframe format.

	Returns:
		result.text -- the returned json as text (because it prints nicer than as json)
	"""
	try:
	 	data = data.to_json(orient='records')
	except Exception:
	 	return AttributeError("Data must be a pandas dataframe")
	result = requests.post(f'{flask_app_url}/predict', json=data)
	return result.text


def main():
	model_info = get_model_info()
	print(model_info)

	feature_names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
	number_of_samples = 5 # how many samples to query the model with
	sample = read_csv('tests/data/test_data.csv', names=feature_names, 
		nrows=number_of_samples, skiprows=random.choice(range(1,20)))
	sample = sample.drop(['class'], axis=1)
	classification = classify_sample(sample)
	print(classification)

if __name__ == '__main__':
	main()
