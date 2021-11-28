FROM tiangolo/meinheld-gunicorn:python3.7

LABEL maintainer="Sankit Acharya <sankit.acharya@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app