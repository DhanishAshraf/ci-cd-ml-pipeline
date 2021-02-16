"""
A function to load the test data to test the model.
To run the file in the terminal run (assuming src is the working directory):
	$ python tests/get_test_data.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import load


def load_data():
	url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
	names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
	dataframe = pd.read_csv(url, names=names)
	return dataframe

def split_data(dataframe, test_size=0.33):
	y = dataframe['class']
	X = dataframe.drop('class', axis=1)
	seed = 7
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
	return X_test, y_test

def save_data(X_test, y_test):
	X_test['class'] = y_test
	X_test.to_csv('tests/data/test_data.csv')

def main():
	# dataframe = load_data()
	# X_test, y_test = split_data(dataframe)
	# save_data(X_test, y_test)
	test_data = pd.read_csv('tests/data/test_data.csv', index_col=0)
	y_test = test_data['class']
	X_test = test_data.drop('class', axis=1)
	# model = load('flask_app/pima_model.joblib')
	# score = model.score(X_test, y_test)
	print(X_test)

if __name__ == '__main__':
	main()