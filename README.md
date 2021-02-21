# A ML pipeline to support CI/CD of ML development. 

Using Google Cloud Platform (GCP) this pipleline will:
	- Store the binary of a machine learning model
	- Run tests against it
	- Promote to production

This pipeline works by automatically triggering a Google Cloud Build job everytime the associated GitHub repository recieves a push and provided the tests pass the machine learning model will be deployed as a Flask application within a Docker container on Google Cloud Run.

Directory Tree:

```
EvolveExpertEx4/
└── src/
	│--- README.md
	│--- cloudbuld.yaml    
	│--- Dockerfile
	│--- requirements.txt
	└───flask_app/
	│   │--- app.py
	│   │--- pima_model.joblib  
	└───tests/
	    │--- example_curl_request.sh
	    │--- get_test_data.py
	    │--- model_tests.py
	    │--- test_requirements.txt
	    └─── data/
``` 


### How To Run:

	1. Create a GCP project (see https://support.google.com/googleapi/answer/6251787?hl=en#) with Cloud Build, Container Registry, Cloud Run and Resource Manager APIs enabled. 
	This can be done by searching for them within the GCP Console (https://console.cloud.google.com/) and clicking 'Enable'.

		For more details on the GCP services:
			* Cloud Build: Orchestates the entire pipleine - https://cloud.google.com/build#section-5
			* Container Registry: Store, manage and secure Docker container images - https://cloud.google.com/container-registry
			* Cloud Run: A managed serverless platform to deploy containerizer applications - https://cloud.google.com/run


	2. Create a new GitHub repository and leave it empty for now. 
	This repository will allow Cloud Build to access the the necessary files.

	3. Next create the Cloud Build GitHub Trigger which will listen to the GitHub repository you just created for a Git Push execution. This will then trigger the execution of the cloudbuild.yaml file which will start the build, test and deploy of the container application. 
			To create the trigger, follow the instructions here:
				https://cloud.google.com/build/docs/automating-builds/create-github-app-triggers
			For the trigger settings:
				Event: Push to a branch
				Source: 
					Branch: ^main$
				Build configuration:
					File type: Cloud Build configuration file (yaml or json)
					Cloud Build configuration file location: cloudbuild.yaml

	4. Cloud Build needs limited permissions to automatically deploy to a Cloud Run Serice. 
			Follow the instruction here: 
				https://cloud.google.com/build/docs/deploying-builds/deploy-cloud-run#console

			Now the trigger is setup, whenever a git push is executed to the git repository, Cloud Build will execute the cloudbuild.yaml file and deploy the containerized ML model.
			The cloudbuild.yaml file consists of 5 steps:
					Step 1. Install the python requirements in order to be able to run the pytests (python tests) on the ML model
					Step 2. Run the pytests to check the ML model is fit for deployment
					Step 3. Build the Docker Image which contains a Python Flask application to expose the ML model as an API
					Step 4. Push the Docker image to Google Container Registry
					Step 5. Deploy the Docker image as an application
			For more details on the cloudbuild config file see: https://cloud.google.com/build/docs/build-config

	5. To get the test set, on your local machine run:
		`src $ python3.7 tests/get_test_data.py`
	This will download and save the test data for you in the tests/data directory.

	6. Push the contents of this directory to your GitHub repository.
	This will trigger the Cloud Build process. The first time make take a while.
	You can view the status of the Cloud Build process in the console by going to Cloud Build > History - https://console.cloud.google.com/cloud-build/builds (make sure you are in the right project)
	Once it is done you will see a green tick next to the build.

	7. In cloud console go to Cloud Run to see your running services - https://console.cloud.google.com/run
	Click on the diabetes-classifier service and the URL for the service is at the top. You need this for the next step.

	8. To query the model:
		i. Activate Cloud Shell in the GCP console - see https://cloud.google.com/shell/docs/using-cloud-shell
		ii. In the shell run the following command:
		`$ curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
		 -H "Content-Type: application/json" \
		 -X POST \
		 -d '{"preg":1,"plas":90,"pres":62,"skin":12,"test":43,"mass":27.2,"pedi":0.58,"age":24}' <app_url>/predict`
		 where app_url is the url from the previous step.







