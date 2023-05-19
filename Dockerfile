FROM python:3.10

WORKDIR /workspace/development

COPY ./requirements.txt /workspace/development/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /workspace/development/requirements.txt


COPY ./app /workspace/development/app
COPY ./Pokemon.json /workspace/development/Pokemon.json