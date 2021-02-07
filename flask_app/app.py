from flask import Flask, request, jsonify
from joblib import load
from pandas import DataFrame

# the names of the features that the model is expecting
feature_names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

# load model
model_filename = 'pima_model.joblib'
loaded_model = load(model_filename)

# create app object
app = Flask(__name__)

# a GET method to identify what model is running here - model cards would be a good idea
@app.route('/', methods=['GET'])
def model_identity():
	return "You can find my source code here: <GitHub Repo>"

# a POST method to make predictions - also ensures the correct features are present first
@app.route('/predict', methods=['POST'])
def make_prediction():
	content = request.json

	try:
		features = DataFrame(data=[content])
		features = features[feature_names]
	except:
		return jsonify(status='error', predict=-1)

	prediction = loaded_model.predict(features)

	return jsonify(status='success', predict=prediction)

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)