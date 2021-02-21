# An example curl request to query the model. Assumes Docker container is running on Google Cloud Run
# In the curl command <app_url> should be replaced by the URL for the running Docker container - See README.md

#!/bin/sh

curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -X POST -d '{"preg":1,"plas":90,"pres":62,"skin":12,"test":43,"mass":27.2,"pedi":0.58,"a
ge":24}' <app_url>/predict
