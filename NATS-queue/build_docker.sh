#! /bin/bash
#
# NATS Queue with Configuration
# =============================================================================
# Build docker image
# =============================================================================

IMAGE_NAME="nats-adroffner"
TAG="latest"

DOCKERFILE=Dockerfile

FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

docker build -t $FULL_IMAGE_NAME ./ \
    --build-arg http_proxy=$http_proxy \
    --build-arg https_proxy=$https_proxy \
    -f ${DOCKERFILE}
