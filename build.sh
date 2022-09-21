#!/bin/bash
#
# This file is part of sensor-harm Docker.
# Copyright (C) 2021-2022 INPE.
#
# sensor-harm Docker is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

set -eou pipefail

#
# General functions
#
usage() {
    echo "Usage: $0 [-n] [-v <2.9.0>] [-b ubuntu:18.04]" 1>&2;

    exit 1;
}

#
# General variables
#
BASE_IMAGE="ubuntu:ubuntu@sha256:122f506735a26c0a1aff2363335412cfc4f84de38326356d31ee00c2cbe52171" # ubuntu:18.04
BUILD_MODE=""
VERSION="latest"
IMAGENAME="brazildatacube/sensor-harm"

#
# Get build options
#
while getopts "b:nv:h" o; do
    case "${o}" in
        b)
            BASE_IMAGE=${OPTARG}
            ;;
        n)
            BUILD_MODE="--no-cache"
            ;;
        v)
            VERSION=${OPTARG}
            IMAGENAME="${IMAGENAME}:${VERSION}"
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

#
# Build a Linux Ubuntu image with all the dependencies already installed
#
echo "Building brazildatacube/sensor-harm Image"
echo "${PWD}"

docker build ${BUILD_MODE} \
       --build-arg ${BASE_IMAGE} \
       -t "${IMAGENAME}:${VERSION}" \
       --file ./docker/Dockerfile .