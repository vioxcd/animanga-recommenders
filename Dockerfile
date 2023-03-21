FROM python:3.10-slim-bullseye
LABEL maintainer="Uchan <ruslanuchan97@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
      && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
      && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
      && apt-get clean \
      && groupadd -g "${GID}" python \
      && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
      && chown python:python -R /app

USER python

COPY --chown=python:python requirements*.txt ./
COPY --chown=python:python . .

ENV PATH /home/python/.local/bin:${PATH}
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

