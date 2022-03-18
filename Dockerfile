# Base Image that includes Lambda Runtime API:
# Source: https://hub.docker.com/r/amazon/aws-lambda-python
FROM amazon/aws-lambda-python:3.8

# Optional: ensure that pip is up to date
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

# first we COPY only the requirements.txt to ensure that later builds with changes to your src code will be faster due to caching of this layer
COPY requirements.txt .
RUN yum update -y
RUN yum install -y libsndfile
RUN pip install -r requirements.txt

# copy all custom modules and files from the src directory
COPY src/ .

RUN pip install --upgrade tensorflow


# specify lambda handler that will be invoked on container start
CMD ["app.handler"]
