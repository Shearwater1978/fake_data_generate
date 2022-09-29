FROM python:3.8.11-bullseye

MAINTAINER Aleksandr uglykoyote@gmail.com

ENV PERSON_COUNT=10

ARG USERNAME=notroot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install net-tools \
    && rm -rf /var/lib/apt/lists /tmp/

USER notroot
WORKDIR /opt/
COPY ./aux_scripts/requirements.txt .
RUN pip install -r ./requirements.txt --no-warn-script-location

WORKDIR /app
COPY ./aux_scripts/ /app/

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
