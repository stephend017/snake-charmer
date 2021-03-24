# FROM ubuntu:latest

# RUN apt-get update -y && \
#     apt-get install -y python3-pip python3-dev

# RUN apt update -y && \
#     apt install git -y

# COPY ./requirements.txt /requirements.txt

# WORKDIR /

# RUN pip3 install -r requirements.txt

# COPY . /

# RUN python3 /setup.py install

# ENTRYPOINT [ "python3" ]

# CMD ["/snake_charmer/__main__.py"]

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

RUN pip install .

# command to run on container start
CMD [ "python", "./snake_charmer/__main__.py" ]
