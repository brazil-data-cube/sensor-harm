# ubuntu:18.04
ARG BASE_IMAGE=ubuntu:ubuntu@sha256:122f506735a26c0a1aff2363335412cfc4f84de38326356d31ee00c2cbe52171
FROM ${BASE_IMAGE}
LABEL maintainer="Brazil Data Cube Team <brazildatacube@inpe.br>"

# Setup build env for PROJ
USER root
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing --no-install-recommends \
            software-properties-common build-essential ca-certificates \
            git make cmake wget unzip libtool automake \
            zlib1g-dev libsqlite3-dev pkg-config sqlite3 libcurl4-gnutls-dev \
            libtiff5-dev \
    && apt install python3-pip -y \
    && apt install nano \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools && pip3 install wheel

RUN mkdir /app

# sensor-harm
COPY . /app/sensor_harm
WORKDIR /app/sensor_harm

RUN pip3 install .

RUN mkdir /code

COPY docker/entrypoint.py /code

WORKDIR /work

### Run the sen2cor application
ENTRYPOINT ["python3", "/code/entrypoint.py"]