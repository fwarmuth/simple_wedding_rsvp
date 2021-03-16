FROM python:3.9-slim

RUN pip install pipenv

ENV SRC_DIR /usr/local/src/rsvp
ENV PYTHONPATH /usr/local/src/rsvp

WORKDIR ${SRC_DIR}

COPY Pipfile Pipfile.lock ${SRC_DIR}/

RUN pipenv install --system --clear

COPY ./ ${SRC_DIR}/

CMD ["flask", "run", "-h", "0.0.0.0"]
