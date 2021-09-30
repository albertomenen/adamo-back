FROM ubuntu:bionic

WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND=noninteractive

#Add requirement files into the image
COPY requirements.txt /usr/src/app

#Update alpine components and dependencies
RUN apt update
RUN apt -y upgrade
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev curl
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python3 get-pip.py
RUN apt install -y python3-opencv
RUN apt-get install -qqy x11-apps
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uwsgi", "--master", "--http", "0.0.0.0:5000", "--processes", "4", "--threads", "2", "--module", "app:app"]
