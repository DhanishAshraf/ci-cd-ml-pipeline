# An example curl request to query the model. Assumes Flask application is running.
# To run: src $ sh tests/example_curl_request.sh

#!/bin/sh

curl -H "Content-Type: application/json" -X POST -d '{"preg":1,"plas":90,"pres":62,"skin":12,"test":43,"mass":27.2,"pedi":0.58,"age":24}' http://0.0.0.0:8080/predict
