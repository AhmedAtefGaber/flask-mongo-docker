# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
COPY app.py .
RUN pip3 install Flask pymongo
RUN pip3 freeze | grep Flask >> requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
