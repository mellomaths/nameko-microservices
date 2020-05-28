FROM python:3.7

WORKDIR /usr/src/app

ADD ./config.yml /usr/src/app
ADD ./Pipfile /usr/src/app/
ADD ./Pipfile.lock /usr/src/app/
ADD ./run.sh /usr/src/app/
COPY . /usr/src/app/

RUN pip install pipenv
RUN pipenv install --sequential --system

RUN chmod +x /user/src/app/run.sh

EXPOSE 8000

CMD [ "/usr/src/app/run.sh" ]
