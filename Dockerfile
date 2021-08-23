FROM python:3.8
RUN mkdir /usr/src/app/
COPY ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["uwsgi", "--master", "--http", "0.0.0.0:5000", "--module", "app:app"]
