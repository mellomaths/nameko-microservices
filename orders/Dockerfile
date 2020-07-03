FROM python:3.8-slim

WORKDIR /usr/src/app

ADD ./config.yml /usr/src/app
ADD ./Pipfile /usr/src/app
ADD ./Pipfile.lock /usr/src/app
ADD ./run.sh /usr/src/app

COPY ./alembic.ini /usr/src/app
COPY ./alembic/ /usr/src/app/alembic/

COPY . .

RUN pip install --upgrade pip
RUN pip install pipenv

RUN apt-get update && apt-get install -y netcat

# RUN apt-get update
# RUN apt-get install -y --no-install-recommends gcc python3-dev libssl-dev

RUN pipenv install --system --deploy --ignore-pipfile

# Making a smaller python image
# RUN apt-get remove -y gcc python3-dev libssl-dev
# RUN apt-get autoremove -y 
# RUN pip uninstall pipenv -y

RUN chmod +x /usr/src/app/run.sh

EXPOSE 8000

CMD [ "/usr/src/app/run.sh" ]
