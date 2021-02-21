""" A simple flask application to serve the Model as an API.
This application has not been fully tested and is just meant to serve as a simple way to host a model 
for basic inputs.

To run: src/flask_app $ python3.7 app.py

Python version: 3.7.3
"""

from flask import Flask, request, jsonify
from joblib import load
from pandas import DataFrame
from json import loads

# Where should the application run
host='0.0.0.0'
port=8080

# load model
model_filename = 'pima_model.joblib'
try:
	loaded_model = load(model_filename)
except FileNotFoundError as e:
	raise FileNotFoundError(f'{model_filename} not found')

# expected input form
expected_input_form = '''{"preg":x, "plas":x,"pres":x,"skin":x,"test":x,"mass":x,"pedi":x,"age":x}'''

# create app object
app = Flask(__name__)


@app.route('/', methods=['GET'])
def model_identity():
	""" A GET method to identify what model is running here.
	Model cards would be a good idea from a governance perspective.
	"""
	return "You can find my source code here: <GitHub Repo>"

 
@app.route('/predict', methods=['POST'])
def make_prediction():
	""" A POST method to make predictions.
	If the request is from Python then request.get_json() returns a json formatted string which needs 
	to be converted to json formatted list.
	If request is from Curl then request.get_json() returns a dict which pandas.DataFrame only accepts
	within a list.
	
	Returns:
	If successful returns output of model as json else a helpful error message as json
	"""
	
	try:
		data = request.get_json()
		data = loads(data) if (type(data)) is str else [data] # details in function docs.
		data = DataFrame(data=data) # put data in the right format for the model
	except Exception:
		return jsonify(Error=f'Input must be of the form: {expected_input_form}') 
	
	try:
		prediction = loaded_model.predict(data)
		prediction = prediction.tolist() # model returns a numpy array which is not json serializable - convert to list
		return jsonify(status='success', prediction=prediction)
	except ValueError:
		return jsonify(ValueError='Expecting 8 features per sample.')
	except:
		return jsonify(Error='Something went wrong.')

	

if __name__=='__main__':
	app.run(debug=True, host=host, port=port)