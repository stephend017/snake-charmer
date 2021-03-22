FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN apt update -y && \
    apt install git -y

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

RUN python3 /setup.py install

ENTRYPOINT [ "python3" ]

CMD ["/snake_charmer/__main__.py"]
