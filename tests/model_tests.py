"""
PyTest to test the model before promoting model to production.
If tests fail the cloud build procedure will fail.
This script assumes you have already run the get_test_data.py file to get the test data.

An example test to ensure the latest model is at least as good as the original model.
Other tests could include checking for bias, looking at accuracy scores in more detail
(e.g. confusion matrix) and testing privacy concerns (is model leaking sensitive training data).

To run: $ pytest tests/model_tests.py

Python version: 3.7.3
"""

import pandas as pd
from joblib import load
import pytest


class TestModel:
	"""A class to include all pytests for model"""
	def load_data(self):
		"""Load the test data"""
		test_data = pd.read_csv('tests/data/test_data.csv', index_col=0)
		self.y_test = test_data['class']
		self.X_test = test_data.drop('class', axis=1)

	def load_model(self):
		"""Load the model to test it"""
		self.model = load('flask_app/pima_model.joblib')

	def test_model_performance(self):
		"""Test if model is atleast as good as original model on test data"""
		self.load_data()
		self.load_model()
		threshold = 0.78 #0.78 to pass - change to 0.90 to deliberate fail test and therefore faild cloud build
		score = self.model.score(self.X_test, self.y_test)
		is_above_threshold = True if score >= threshold else False
		assert is_above_threshold is True

		
			


