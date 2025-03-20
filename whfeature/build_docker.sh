#!/usr/bin/env bash
docker build -t feature_build:redhat7 -f docker/Dockerfile.redhat7 .
#docker build -t feature_build:redhat8 -f docker/Dockerfile.redhat8 .
#docker build -t feature_build:ubuntu2404 -f docker/Dockerfile.ubuntu2404 .
#docker build -t feature_build:ubuntu2204 -f docker/Dockerfile.ubuntu2204 .