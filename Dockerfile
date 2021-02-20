# use the space saving python 3.7 image from hub.docker.com
FROM python:3.7-slim-buster

# copy over the requirements.txt file which has the required python packages
COPY requirements.txt .

# update pip
RUN pip install --upgrade pip
# install requirements
RUN pip install -r requirements.txt

# copy over the flask app
COPY flask_app flask_app/

# set the working directory
WORKDIR flask_app

# which port will be published
EXPOSE 8080

# starts the flask application
CMD ["python", "app.py"] 