FROM python:3.8-slim-buster as base

FROM base as builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt


FROM base
ENV PIP_NO_CACHE_DIR=1
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y netcat

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /usr/src/app/run.sh

EXPOSE 8000

ENTRYPOINT [ "/usr/src/app/run.sh" ]
