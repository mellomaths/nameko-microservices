FROM python:3.8-slim-buster as builder

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt


FROM python:3.8-slim-buster
ENV PIP_NO_CACHE_DIR=1
RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/src/app/run.sh

EXPOSE 8000

ENTRYPOINT [ "/usr/src/app/run.sh" ]