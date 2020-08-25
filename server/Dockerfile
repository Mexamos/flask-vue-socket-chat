FROM python:3.7-slim-buster

RUN apt update
RUN apt install -y build-essential

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY app.py .
COPY uwsgi.ini .

RUN addgroup --system --gid 1000 www
RUN adduser --system --no-create-home --shell /bin/bash --uid 1000 --gid 1000 www
RUN chown -R www:www /app

USER www

EXPOSE 5000

CMD ["uwsgi", "uwsgi.ini"]
