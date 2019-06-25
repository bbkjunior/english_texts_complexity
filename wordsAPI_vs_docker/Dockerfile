FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /wordsAPI

WORKDIR /wordsAPI

ADD . /wordsAPI/

EXPOSE 1337

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:1337"]
