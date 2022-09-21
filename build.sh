#!/bin/bash
#
# This file is part of Brazil Data Cube sensor-harm.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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