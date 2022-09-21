# This file is part of Brazil Data Cube sensor-harm.
# Copyright (C) 2022 INPE.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.

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